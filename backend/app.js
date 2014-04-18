var app = require('express')()
  , server = require('http').createServer(app)
  , io = require('socket.io').listen(server)
  , path = require('path')
  , redis = require('redis')
  , redis_client = redis.createClient();

var INDEX_FILE = "../heatmap/index.html";

io.set('log level', 2); // Info only

server.listen(80);

redis_client.on("error", function (err) {
    console.log("Error " + err);
});

var enableCORS = function(req, res, next) {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS');
    res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization, Content-Length, X-Requested-With');

    // intercept OPTIONS method
    if ('OPTIONS' == req.method) {
      res.send(200);
    }
    else {
      next();
    }
};

app.use(enableCORS);

app.options('/', function(req, res){ 
    console.log("writing headers only"); 
    res.header("Access-Control-Allow-Origin", "*"); 
    res.end(''); 
});

app.get('/', function (req, res) {
  res.sendfile(path.resolve(INDEX_FILE));
});

io.sockets.on('connection', function (socket) {
  var random_emitter = function() {
    socket.volatile.emit('newPoint', randomPoint());
  };

  var redis_emitter = function() {
    redis_client.brpoplpush("sentiment_stream", "sentiment_stream", 0, function(err, reply) {
      var point = JSON.parse(reply);
      socket.volatile.emit('newPoint', point);
    });
  };

  var emit_interval = setInterval(redis_emitter, 20);
  socket.on('disconnect', function() {
    clearInterval(emit_interval);
  });
});

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

