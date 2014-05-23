// site.js
// dependencies: app.js

$(document).ready(function() {
    window.newTopicsCount = 0;
    window.topicInfo = {};

    // App evet handlers
    var topicHandler = function(topicPoint) {
        var topic = topicPoint.topic;

        // Update topic rating view
        if (window.topicInfo[topic]) {
            if (topicPoint.sentiment > 0) {
                window.topicInfo[topic].numPositive++;
            }
            window.topicInfo[topic].numTotal++;

        } else {
            var $li = $('<li class="topic-item"></li>');
            var $a = $('<a href="#">' + topic + '</a>');
            var $progressBar = $('<div class="progress topic-rating-bars"></div>');
            var $positiveBar = $('<div class="progress-bar progress-bar-success" style="width: 0%"></div>');
            var $negativeBar = $('<div class="progress-bar progress-bar-danger" style="width: 0%"></div>');

            window.topicInfo[topic] = {};
            window.topicInfo[topic].numPositive = topic.sentiment > 0 ? 1 : 0;
            window.topicInfo[topic].numTotal = 1;
            window.topicInfo[topic].$li = $li;
            window.topicInfo[topic].$positiveBar = $positiveBar;
            window.topicInfo[topic].$negativeBar = $negativeBar;

            $('#topic-menu').append($li);
            $li.append($a);
            $a.append($progressBar);
            $progressBar.append($positiveBar);
            $progressBar.append($negativeBar);

            $a.on('click', function(topic, $li) {
                return function(e) {
                    window.app.switchTopic(topic);
                    $('.topic-item').removeClass("active");
                    $li.addClass("active");
                    e.preventDefault();
                };
            }(topic, $li));

            // update new topic count
            window.newTopicsCount += 1;
            // $('#new-topics-badge').text(window.newTopicsCount);
            // $('#new-topics-badge').show();
        }

        // Update topic's sentiment meter
        window.topicInfo[topic].$positiveBar.width(window.topicInfo[topic].numPositive / window.topicInfo[topic].numTotal * 100 + "%");
        window.topicInfo[topic].$negativeBar.width((window.topicInfo[topic].numTotal - window.topicInfo[topic].numPositive) / window.topicInfo[topic].numTotal * 100 + "%");
    };

    var newRate = function(rate) {
        $('#rateText').text(rate + " points/second.");
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
        $("#no-topic-topic-item").on("click", function() {
            window.app.switchTopic();
            $('.topic-item').removeClass("active");
            $(this).addClass("active");
        });
        $("#no-topic-topic-item a").on("click", function() {
            e.preventDefault();
        });

        $("#heatmap-mode-btn").on("click", function (e) {
            $("#states-mode-btn").removeClass('selected-map-view');
            $("#heatmap-mode-btn").addClass('selected-map-view');
            window.app.switchView('heatmap');
            e.preventDefault();
        }); 
      
        $("#states-mode-btn").on("click", function (e) {
            $("#heatmap-mode-btn").removeClass('selected-map-view');
            $("#states-mode-btn").addClass('selected-map-view');
            window.app.switchView('states');
            e.preventDefault();
        }); 
    } else {
        $('#error-messages').append('<div class="alert alert-danger">Error! Cannot connect to server. Please try again.</div>');
    }

    // App view event bindings that don't depend on connection

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
