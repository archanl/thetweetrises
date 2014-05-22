// site.js
// dependencies: app.js

$(document).ready(function() {
    // App evet handlers
    var newTopic = function(topic, changeTopicHandler) {
        var $li = $('<li></li>');
        var $a = $('<a href="#" class="channelLink unseen">' + topic + '</a>');

        $('#topic-menu').append($li);
        $li.append($a);

        /*var f = function(x) {
            return function() {
                window.app.changeTopic(x);
            };
        };*/
        $channelLink.find('a').on('click', changeHandler);
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

    window.app.connect("http://162.243.150.138");


    // App interaction hooks

    $("#heatmap-mode-btn").on("click", function () {
        window.app.switchView('heatmap');
    }); 
  
    $("#states-mode-btn").on("click", function () {
        window.app.switchView('states');
    }); 
  
    $("#topics-dropdown").click(function () {
        var g = function(x) {
            return function() {
                window.app.newTopicsCount -= x;
                $('#new-topics-badge').text(newTopicsCount > 0 ? newTopicsCount : '');
                $('.unseen').removeClass("unseen");
            };
        };
        setTimeout(g(window.app.newTopicsCount), 2500);
    });
  
    $('.dropdown').on('click', '.channelLink', function () {
        $('.channelLink').removeClass("selected-channel");
        $(this).removeClass("unseen");
        $(this).addClass("selected-channel");
    });
  
    $('.navbar-nav').on('click', 'a', function(e) {
        e.preventDefault();
    });

    $('#fullscreen-button').click(function() {
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
    });
});
