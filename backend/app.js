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
// TODO: Is it OK to have global variables? what happens when multiple users login?
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
    // TODO: Check this, emitting very rarely
    redis_client.zrange("sentiment_stream", 0, -1, function(err, reply) {
      var point = JSON.parse(reply);
      point.topic = null;
      // Only emit if different from last message
      if (last_emitted.latitude !== point.latitude) {
          last_emitted = point;
          socket.volatile.emit('newPoint', point);
      }

      // Emit a single tweet from all trends
      redis_client.zrange("trending_keys", 0, -10, function(err, reply) {
        
          for (var i=0; i < reply.length; i++) {
              var trend = reply[i];
              redis_client.zrange("trending:".concat(trend), 0, -1, function(err, reply) {
                  var point = JSON.parse(reply);
                  point.topic = trend;
                  socket.volatile.emit('initialPoints', point);
              });
          }
    });

    });
  };

  // Initial emits
  var initial_emit = function() {
      var d = new Date();
      var now = d.getTime();
      redis_client.zrange("sentiment_stream", now, now - 600, function(err, reply) {
          var point = JSON.parse(reply);
          point.topic = null;
          socket.volatile.emit('initialPoints', point);
      
      });

      
      redis_client.zrange("trending_keys", 0, -10, function(err, reply) {
        
          // Emit last 600 secs from each trend
          for (var i=0; i < reply.length; i++) {
              var trend = reply[i];
              redis_client.zrange("trending:".concat(trend), 0, -200, function(err, reply) {
                  var point = JSON.parse(reply);
                  point.topic = trend;
                  socket.volatile.emit('initialPoints', point);
              });
          }
    });

  };

  var emit_interval = setInterval(redis_emitter, 20);
  socket.on('disconnect', function() {
    clearInterval(emit_interval);
  });

});


function emitTrendingJSON() {
  redis_client.get("trending_json", function(err, reply) {
    io.sockets.emit('trending', reply);
  });
}

setInterval(emitTrendingJSON, 5000);

function getTrendingTopics() {
    var args = ["+inf", "-inf", "WITHSCORES", "LIMIT", 0, 5];
    redis_client.zrevrangebyscore(args, function(err, reply) {
        var trending = "";
        // The trending topics will be in the even indeces of the array
        for (i = 0; i < reply.size(); i += 2) {
            trending += reply[i];
        }
        console.log(trending);
    })
    // TODO: serve

}

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

