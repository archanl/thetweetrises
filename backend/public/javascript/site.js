// site.js
// dependencies: app.js

$(document).ready(function() {
    window.newTopicsCount = 0;

    // App evet handlers
    var newTopic = function(topic, changeTopicHandler) {
        var $li = $('<li></li>');
        var $a = $('<a href="#" class="channelLink unclicked">' + topic + '</a>');
        $('#topic-menu').append($li);
        $li.append($a);
        $a.on('click', function() {
            console.log('changing Topic, calling handler');
            changeTopicHandler();
            $('.channelLink').removeClass("selected-channel");
            $(this).removeClass('unclicked');
            $(this).addClass("selected-channel");
        });

        window.newTopicsCount += 1;
        $('#new-topics-badge').text(window.newTopicsCount);
        $('#new-topics-badge').show();
    };

    var newRate = function(rate) {
        $('#rateText').text("Data download rate: " + rate + " points/second.");
    };

    // App initialization

    window.app = new TweetRisesApp({
        mapCanvasId: 'map-canvas',
        newTopicHandler: newTopic,
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
            window.app.switchTopic('');
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
