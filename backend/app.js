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
var last_time = new Date().getTime();

function ten_second_emitter() {
  // Update last_time
  var lt = last_time;
  var now = new Date().getTime());
  last_time = now;

  // Emit sentiment_stream
  redis_client.zrangebyscore("sentiment_stream", lt, now, function(err, reply) {
    console.log("ten_second_emitter : sentiment_stream ::");
    console.log(reply);

    if (!reply) {
      return;
    }

    io.sockets.emit('newPoints', reply);
  });

  // Emit trending topics
  redis_client.zrevrange("trending_keys", 0, 10, function(err, keys_reply) {
    console.log("ten_second_emitter : trending-keys ::");
    console.log(keys_reply);

    if (!keys_reply) {
      return;
    }

    // For each trending topic
    for (var i=0; i < keys_reply.length; i++) {
      console.log("getting trend " + i);
      var trend = keys_reply[i];
      console.log('trend is ' + trend);

      !function(trend, now) {
        redis_client.zrangebyscore("trending:" + trend, lt, now, function(err, trend_reply) {
          console.log("ten_second_emitter : trending-keys : trending:" + trend + " ::");
          console.log(trend_reply);

          if (!trend_reply) {
            return;
          }

          for (var j = 0; j < trend_reply.length; j++) {
            var point = trend_reply[j];

            point.topic = trend;
            io.sockets.emit('newPoint', point);
          }
        });
      }(trend, now);
    }
  });
}

var ten_second_interval = setInterval(ten_second_emitter, 10000);

//////////////////////////////////////////////////////////////////////////////
// Socket connection handler
////////////////////////////
io.sockets.on('connection', function (socket) {
  var now = new Date().getTime();

  // Emit initial points for sentiment_stream
  redis_client.zrangebyscore("sentiment_stream", now - 600000, now - 10000, function(err, reply) {
    console.log("initial_emission : sentiment_stream ::");
    console.log(reply);

    if (reply) {
      socket.emit('newPoints', reply);
    }
  });

  // Emit initial points for trending topics
  redis_client.zrevrange("trending_keys", 0, 10, function(err, keys_reply) {
    console.log("initial_emission : trending-keys ::");
    console.log(keys_reply);

    if (!keys_reply) {
      return;
    }
    
    // For each trending topic
    for (var i = 0; i < keys_reply.length; i++) {
      console.log("getting trend " + i);
      var trend = keys_reply[i];
      console.log('trend is ' + trend);

      !function(trend, now) {
        redis_client.zrangebyscore("trending:" + trend, now - 600000, now - 10000, function(err, trend_reply) {
          console.log("initial_emission : trending-keys : trending:" + trend + " ::");
          console.log(trend_reply);

          if (!trend_reply) {
            return;
          }

          for (var j = 0; j < trend_reply.length; j++) {
            var point = trend_reply[j];
            point.topic = trend;
            io.sockets.emit('newPoint', point);
          }
        });
      }(trend, now);
    }
  });
});

//////////////////////////////////////////////////////////////////////////////
// Start server
///////////////
server.listen(80);