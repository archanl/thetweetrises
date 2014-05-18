/*
var stateAverages = false;

var topicPoints = {"average":[]};
var specificTopic = false;
var currentFilter = null;

var numberToAverage = 5;


function addPoint(data) {
    if (data) {
      storeAllStatePoints(data, 100);

      if (data.topic){
        console.log('point has topic: ' + data.topic);
        if (topicPoints[data.topic]){
          topicPoints[data.topic].push(data);
        }
        else{
          topicPoints[data.topic] = [];
          topicPoints[data.topic].push(data);
          var $channelLink = $('<li><a href="#" class="channelLink unseen">' + data.topic + '</a></li>');
          $('#topic-menu').append($channelLink);

          var f = function(x) {
            return function() {
              changeTopic(x);
            };
          };
          $channelLink.find('a').on('click', f(data.topic));
        }
      }
      else{
        topicPoints["average"].push(data);
      }

      var latlng = new google.maps.LatLng(data.latitude, data.longitude);

      if (data.sentiment > 0) {
          pointArray.push(latlng);
      }
      else {
          pointArrayNeg.push(latlng);
      }
      numTotalReceivedPoints++;
      //addStatePoints(data, stateAverages);
      if (specificTopic == false){
        addStatePoints2(data, numberToAverage);
      }
      else{
        if (data.topic == currentFilter){
          addStatePoints2(data, numberToAverage);
        }
      }
    }
}

function addPoints(data) {
  if (!data) {
    return;
  }

  console.log('addpoints() data length: ' + data.length);

  for (var i = 0; i < data.length; i++) {
    addPoint(data[i]);
  }
}

function changeTopic(topicName) {
    console.log('changeTopic(' + topicName + ')')
    specificTopic = true;
    currentFilter = topicName;
    clearStateLists();
    if (topicPoints[topicName]){
      for (i = 0; i < topicPoints[topicName].length; i++){
        addStatePoints2(topicPoints[topicName][i], numberToAverage);
      }
    }
}

function viewAllTopics() {
    var specificTopic = false;
    var currentFilter = null;
    clearStateLists();
    showAllPointsAgain(numberToAverage);
}




function HeatmapMode() {
  heatmap.setMap(map);
  heatmapNeg.setMap(map);
  //disableStatesMode();
}

function switchModeAverage() {
    heatmap.setMap(null);
    heatmapNeg.setMap(null);
    stateAverages = true;
    enableStatesMode(stateAverages);
}

function switchModeCurrent() {
    heatmap.setMap(null);
    heatmapNeg.setMap(null);
    stateAverages = false;
    enableStatesMode(stateAverages);
}
*/






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
