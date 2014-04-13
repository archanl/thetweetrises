var app = require('express')()
  , server = require('http').createServer(app)
  , io = require('socket.io').listen(server);

server.listen(80);

app.options('/', function(req, res){ 
    console.log("writing headers only"); 
    res.header("Access-Control-Allow-Origin", "*"); 
    res.end(''); 
});

app.get('/', function (req, res) {
  res.sendfile(__dirname + '/index.html');
});

io.sockets.on('connection', function (socket) {
  var f = function() {
    var np =  {
      latitude: randomLat(),
      longitude: randomLong(),
      emotion: randomEmotion()
    };

    socket.volatile.emit('newPoint', np);
  };

  setInterval(f, 100);
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
