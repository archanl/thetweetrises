// site.js
// dependencies: app.js

$(document).ready(function() {
    window.newTopicsCount = 0;
    window.topicInfo = {};

    // App evet handlers
    var topicHandler = function(topicPoint) {
        var topic = decodeURIComponent(topicPoint.topic);

        // Update topic rating view
        if (window.topicInfo[topic]) {
            if (topicPoint.sentiment > 0) {
                window.topicInfo[topic].numPositive++;
            }
            window.topicInfo[topic].numTotal++;

        } else {
            var $li = $('<li></li>');
            var $a = $('<a href="#" class="channelLink unclicked">' + topic + '</a>');
            var $progressBar = $('<div class="progress topic-rating-bars"></div>');
            var $positiveBar = $('<div class="progress-bar progress-bar-success" style="width: 0%"></div>');
            var $negativeBar = $('<div class="progress-bar progress-bar-danger" style="width: 0%"></div>');

            window.topicInfo[topic] = {};
            window.topicInfo[topic].numPositive = topic.sentiment > 0 ? 1 : 0;
            window.topicInfo[topic].numTotal = 1;
            window.topicInfo[topic].$li = $li;
            window.topicInfo[topic].$a = $a;
            window.topicInfo[topic].$positiveBar = $positiveBar;
            window.topicInfo[topic].$negativeBar = $negativeBar;

            $('#topic-menu').append($li);
            $li.append($a);
            $li.append($progressBar);
            $progressBar.append($positiveBar);
            $progressBar.append($negativeBar);

            $a.on('click', function(topic, $a) {
                return function() {
                    window.app.switchTopic(topic);
                    $('.channelLink').removeClass("selected-channel");
                    $a.removeClass('unclicked');
                    $a.addClass("selected-channel");
                };
            }(topic, $a));

            // update new topic count
            window.newTopicsCount += 1;
            $('#new-topics-badge').text(window.newTopicsCount);
            $('#new-topics-badge').show();
        }

        // Update topic's sentiment meter
        window.topicInfo[topic].$positiveBar.width(window.topicInfo[topic].numPositive / window.topicInfo[topic].numTotal * 100 + "%");
        window.topicInfo[topic].$negativeBar.width((window.topicInfo[topic].numTotal - window.topicInfo[topic].numPositive) / window.topicInfo[topic].numTotal * 100 + "%");
    };

    var newRate = function(rate) {
        $('#rateText').text("Data download rate: " + rate + " points/second.");
    };

    // App initialization

    window.app = new TweetRisesApp({
        mapCanvasId: 'map-canvas',
        topicViewHandler: topicHandler,
        newRateHandler: newRate,
        mapOptions: {
            zoom: 4,
            center: new google.maps.LatLng(39.833333, -98.583333),
            mapTypeId: google.maps.MapTypeId.ROADMAP
        }
    });

    // App view hooks that depend on connection

    if (window.app.connect("http://162.243.150.138")) {
        $("#default-map-link").on("click", function() {
            window.app.switchTopic();
            $('.channelLink').removeClass("selected-channel");
            $(this).removeClass('unclicked');
            $(this).addClass("selected-channel");
        });

        $("#heatmap-mode-btn").on("click", function () {
            window.app.switchView('heatmap');
        }); 
      
        $("#states-mode-btn").on("click", function () {
            window.app.switchView('states');
        }); 
    } else {
        $('#error-messages').append('<div class="alert alert-danger">Error! Cannot connect to server. Please try again.</div>');
    }

    // App view event bindings that don't depend on connection
  
    $('.navbar-nav').on('click', 'a', function(e) {
        e.preventDefault();
    });

    $("#topics-dropdown").click(function () {
        $('#new-topics-badge').text('');
        $('#new-topics-badge').hide();
        window.newTopicsCount = 0;
    });
  

    $('#fullscreen-button').click(function() {
        var center = window.app.map.getCenter();
        var $b = $('body');
        var $btn = $('#fullscreen-button');
        if ($b.hasClass('fullscreen')) {
            $b.removeClass('fullscreen');
            $btn.text('Fullscreen');
            $btn.addClass('btn-primary');
            $btn.removeClass('btn-danger');
        } else {
            $b.addClass('fullscreen');
            $btn.text('Exit');
            $btn.addClass('btn-danger');
            $btn.removeClass('btn-primary');
        }
        google.maps.event.trigger(window.app.map, "resize");
        window.app.map.setCenter(center);
    });
});
