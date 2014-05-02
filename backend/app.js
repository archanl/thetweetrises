var express = require('express')
  , app = express()
  , http = require('http')
  , server = http.createServer(app)
  , socketIO = require('socket.io')
  , io = socketIO.listen(server)
  , path = require('path')
  , redis = require('redis')
  , crypto = require('crypto')
  , _und = require('underscore')
  , redis_client = redis.createClient();

// Initial emit size
var iemit_size = 100;

// Last emitted sentiment
var last_emitted = ""

io.set('log level', 2); // Info only

redis_client.on("error", function (err) {
    console.log("Error " + err);
});

app.use(express.static(__dirname + '/public'));

io.sockets.on('connection', function (socket) {
  var random_emitter = function() {
    socket.volatile.emit('newPoint', randomPoint());
  };

  var redis_emitter = function() {
    redis_client.lrange("sentiment_stream", 0, 0, function(err, reply) {
      var point = JSON.parse(reply);
      // Only emit if different from last message
      if (_und.isEqual(last_emitted, point)) {
          last_emitted = point;
          socket.volatile.emit('newPoint', point);
      }
    });
  };

  var initial_emit = function() {
    redis_client.lrange("sentiment_stream", 0, 100, function(err, reply) {
      var point = JSON.parse(reply);
      socket.volatile.emit('preload_data', point);
      
    });
  };

  var emit_interval = setInterval(redis_emitter, 20);
  socket.on('disconnect', function() {
    clearInterval(emit_interval);
  });

});

server.listen(80);




// Random points generator

var minLat = 29.482843,
    maxLat = 48.972145,
    minLong = -123.119431,
    maxLong = -76.010060;
    
function randomLat() {
    return Math.random() * (maxLat - minLat) + minLat;
}

function randomLong() {
  return Math.random() * (maxLong - minLong) + minLong;
}

function randomEmotion() {
  return (Math.random() > 0.66) ? 1 : 0;
}

function randomPoint() {
  var lat = Math.random(),
      lng = Math.random(),
      emo = Math.random();

  emo = lng > .6 ?
        (emo > .9 ? 1 : 0) :
        (emo > .7 ? 0 : 1);

  lat = lat * (maxLat - minLat) + minLat;
  lng = lng * (maxLong - minLong) + minLong;

  return {
    latitude: lat,
    longitude: lng,
    emotion: emo
  }
}

