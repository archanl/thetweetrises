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
var last_time = Math.floor((new Date().getTime()) / 1000);

function ten_second_emitter() {
  // Update last_time
  var lt = last_time;
  var now = Math.floor((new Date().getTime()) / 1000);
  last_time = now;

  // Emit sentiment_stream
  redis_client.zrangebyscore("sentiment_stream", lt, now, function(err, reply) {
    if (reply) {
      io.sockets.volatile.emit('newPoints', reply);
    }
  });

  // Emit trending topics
  redis_client.zrevrange("trending_keys", 0, 10, function(err, keys_reply) {
    if (!keys_reply) {
      return;
    }

    // For each trending topic
    for (var i=0; i < keys_reply.length; i++) {
      var trend = keys_reply[i];

      !function(trend, lt, now) {
        redis_client.zrangebyscore("topic_sentiment_stream:" + trend, lt, now, function(err, reply) {
          if (reply) {
            io.sockets.emit('newPoints', reply);
          }
        });
      }(trend, lt, now);
    }
  });

  // Emit permanent topics
  redis_client.get("permanent_topics", function(err, permanent_topics_json) {
    if (!permanent_topics_json) {
      return;
    }

    for (topic in JSON.parse(permanent_topics_json)) {
      !function(topic, lt, now) {
        redis_client.zrangebyscore("topic_sentiment_stream:" + topic, lt, now, function(err, reply) {
          if (reply) {
            io.sockets.emit('newPoints', reply);
          }
        });
      }(topic, lt, now);
    }
  });
}

var ten_second_interval = setInterval(ten_second_emitter, 2000);

//////////////////////////////////////////////////////////////////////////////
// Socket connection handler
////////////////////////////
io.sockets.on('connection', function (socket) {
  var now = Math.floor((new Date().getTime()) / 1000);
  var begTime_all = now - 60; // 1 min ago
  var endTime_all = now - 10; // 10 seconds ago
  var begTime_topics = now - 86400; // 24 hours ago
  var endTime_topics = now - 10; // 10 seconds ago

  // Emit initial points for sentiment_stream
  redis_client.zrangebyscore("sentiment_stream", begTime_all, endTime_all, function(err, reply) {
    if (reply) {
      socket.emit('newPoints', reply);
    }
  });

  // Emit initial points for trending topics
  redis_client.zrevrange("trending_keys", 0, 10, function(err, keys_reply) {
    if (!keys_reply) {
      return;
    }
    
    // For each trending topic
    for (var i = 0; i < keys_reply.length; i++) {
      var trend = keys_reply[i];

      !function(trend, begTime_topics, endTime_topics) {
        redis_client.zrangebyscore("topic_sentiment_stream:" + trend, begTime_topics, endTime_topics, function(err, reply) {
          if (reply) {
            socket.emit('newPoints', reply);
          }
        });
      }(trend, begTime_topics, endTime_topics);
    }
  });

  // Emit initial points for permanent topics
  redis_client.get("permanent_topics", function(err, permanent_topics_json) {
    if (!permanent_topics_json) {
      return;
    }

    for (topic in JSON.parse(permanent_topics_json)) {
      !function(topic, begTime_topics, endTime_topics) {
        redis_client.zrangebyscore("topic_sentiment_stream:" + topic, begTime_topics, endTime_topics, function(err, reply) {
          if (reply) {
            socket.emit('newPoints', reply);
          }
        });
      }(topic, begTime_topics, endTime_topics);
    }
  });
});

//////////////////////////////////////////////////////////////////////////////
// Start server
///////////////
server.listen(80);

