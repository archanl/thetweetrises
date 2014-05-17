var express = require('express')
  , app = express()
  , http = require('http')
  , server = http.createServer(app)
  , socketIO = require('socket.io')
  , io = socketIO.listen(server)
  , path = require('path')
  , redis = require('redis')
  , crypto = require('crypto')
  , _ = require('underscore')
  , redis_client = redis.createClient();

//////////////////////////////////////////////////////////////////////////////
// Setup io, redis client, and app
//////////////////////////////////

io.set('log level', 2); // Info only

redis_client.on("error", function (err) {
  console.log("Error " + err);
});

app.use(express.static(__dirname + '/public'));

//////////////////////////////////////////////////////////////////////////////
// Global 10 second emitter
///////////////////////////
var last_time = (new Date()).getTime() / 1000;
function ten_second_emitter() {
  var lt = last_time;
  var now = ((new Date()).getTime() / 1000);
  last_time = now;

  redis_client.zrangebyscore("sentiment_stream", now, lt, function(err, reply) {
    console.log('ten second sentiment stream:');
    console.log(reply);
  });

  redis_client.zrange("trending_keys", 0, -10, function(err, keys_reply) {
    var trend, point;
    console.log('retrieving 10 trending keys:');
    console.log(keys_reply);

    // for (var i=0; i < keys_reply.length; i++) {
    //   trend = keys_reply[i];

    //   redis_client.zrangebyscore("trending:" + trend, now, lt, function(err, trend_reply) {
    //     for (var j = 0; j < trend_reply.length; j++) {
    //       point = JSON.parse(reply);
    //       point.topic = trend;
    //       socket.emit
    //     }
    //     socket.
    //         point.topic = trend;
    //         socket.volatile.emit('initialPoints', point);
    //     });
    // }
  });
}

var ten_second_interval = setInterval(ten_second_emitter, 10000);

//////////////////////////////////////////////////////////////////////////////
// Socket connection handler
////////////////////////////
io.sockets.on('connection', function (socket) {


  // var redis_emitter = function() {
  //   // TODO: Check this, emitting very rarely
  //   redis_client.zrevrange("sentiment_stream", 0, 0, function(err, reply) {
  //     var point = JSON.parse(reply);
  //     point.topic = null;
  //     // Only emit if different from last message
  //     if (last_emitted.latitude !== point.latitude) {
  //         last_emitted = point;
  //         socket.volatile.emit('newPoint', point);
  //     }

  //     // Emit a single tweet from all trends
  //     redis_client.zrange("trending_keys", 0, -10, function(err, reply) {
        
  //         for (var i=0; i < reply.length; i++) {
  //             var trend = reply[i];
  //             redis_client.zrevrange("trending:".concat(trend), 0, 0, function(err, reply) {
  //                   // TODO: This is not parsing, no idea why
  //                 var point = JSON.parse(reply);
  //                 point.topic = trend;
  //                 socket.volatile.emit('initialPoints', point);
  //             });
  //         }
  //   });

  //   });
  // };

  // // Initial emits
  // var initial_emit = function() {
  //     var d = new Date();
  //     var now = d.getTime();
  //     redis_client.zrange("sentiment_stream", now, now - 600, function(err, reply) {
  //         var point = JSON.parse(reply);
  //         point.topic = null;
  //         socket.volatile.emit('initialPoints', point);
      
  //     });

      
  //     redis_client.zrange("trending_keys", 0, -10, function(err, reply) {
        
  //         // Emit last 600 secs from each trend
  //         for (var i=0; i < reply.length; i++) {
  //             var trend = reply[i];
  //             redis_client.zrange("trending:".concat(trend), 0, -200, function(err, reply) {
  //                 var point = JSON.parse(reply);
  //                 point.topic = trend;
  //                 socket.volatile.emit('initialPoints', point);
  //             });
  //         }
  //   });
  // };
});