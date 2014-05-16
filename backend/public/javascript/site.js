// It's usually a good idea to put everything in a function closure so that variable
// names don't conflict with libraries being used

var hostname = "http://162.243.150.138";
//var hostname = "http://localhost:8080/";

var map, pointArray, pointArrayNeg, heatmap, heatmapNeg;

var data = [];

var dataNeg = [];

var topicChannels = [];

var newTopicsCount = 0;

var stateAverages = false;

function initializeMap() {
  var mapOptions = {
    zoom: 4,
    center: new google.maps.LatLng(39.833333, -98.583333),
    mapTypeId: google.maps.MapTypeId.ROADMAP
  };
  map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

  pointArray = new google.maps.MVCArray(data);
}

function initializeHeatmap() {
  var gradientPos = [
    'rgba(255,255,255,0)',
    'rgba(235,229,255,0)',
    'rgba(216,204,255,0)',
    'rgba(197,178,255,1)',
    'rgba(178,153,255,1)',
    'rgba(159,127,255,1)',
    'rgba(140,102,255,1)',
    'rgba(121,76,255,1)',
    'rgba(98,50,255,1)',
    'rgba(101,50,255,1)',
    'rgba(82,25,255,1)',
    'rgba(63,0,255,1)'
  ]
  heatmap = new google.maps.visualization.HeatmapLayer({
    data: pointArray
  });
  heatmap.set('gradient', gradientPos);
  // heatmap.setMap(map);

  pointArrayNeg = new google.maps.MVCArray(dataNeg);

  var gradientNeg = [
    'rgba(255,255,255,0)',
    'rgba(255,229,229,0)',
    'rgba(255,206,207,0)',
    'rgba(255,178,179,1)',
    'rgba(255,153,154,1)',
    'rgba(255,127,129,1)',
    'rgba(255,102,104,1)',
    'rgba(255,76,79,1)',
    'rgba(255,50,54,1)',
    'rgba(255,25,29,1)',
    'rgba(255,0,0,1)'
  ]
  heatmapNeg = new google.maps.visualization.HeatmapLayer({
    data: pointArrayNeg
  });
  heatmapNeg.set('gradient', gradientNeg);
  // heatmapNeg.setMap(map);
}

// Should call every second
var numTotalReceivedPoints = 0;
function updateRate() {
  $('#rateText').text("Data download rate: " + numTotalReceivedPoints + " points/second.");
  numTotalReceivedPoints = 0;
}

// Garbage collection: make old points decay
function gc() {
    // Max number of points per array
    while (pointArray.length + pointArrayNeg.length > 2000) {
      if (pointArray.length) {
        pointArray.removeAt(0);
      }
      if (pointArrayNeg.length) {
        pointArrayNeg.removeAt(0);
      }
      console.log('gc(): Old points have been removed.');
    }
}

function initializeSocket() {
    var socket = io.connect(hostname);
    
    // Initialize rate counter
    window.setInterval(updateRate, 1000);

    // Initialize garbage collection
    window.setInterval(gc, 5000);

    socket.on("newPoint", addPoint);
    socket.on("initialPoints", prePopulate);
    socket.on("trending", changeTrending);
}

function addPoint(data) {
    if (data) {
      var emotion = data.sentiment > 0 ? 1 : 0;
      var lat = data.latitude;
      var lng = data.longitude;
      var latlng = new google.maps.LatLng(lat,lng);

      if (emotion == 0) {
          pointArray.push(latlng);
      }
      else {
          pointArrayNeg.push(latlng);
      }
      numTotalReceivedPoints++;
      addStatePoints(data, stateAverages);
    }
}

function prePopulate(data) {
    // Add every point to the heatmap
    for (var i = 0; i < data.length; i++) {
        var p = data[i];
        var lat = p.latitude;
        var lng = p.longitude;
        var latlng = new google.maps.LatLng(lat,lng);

        if (p.emotion == 0) {
            pointArray.push(latlng);
        }
        else {
            pointArrayNeg.push(latlng);
        }
       // p.sentiment = p.emotion;
       // addStatePoints(p);
    }
}

function switchChannel(channel) {
  console.log('Switching to Channel: ' + topicChannels[channel].name);
  //todo
}
function changeTrending(data) {
  if (data) {
    var obj = JSON.parse(data);
    for (var i = 0; i < 10; i++){
      var trend = obj[0].trends[i];

      if (!topicChannels[i] || (topicChannels[i].name !== trend.name)) {
        newTopicsCount = newTopicsCount + 1 > 10 ? 10 : newTopicsCount + 1;
        $('#new-topics-badge').text(newTopicsCount);

        topicChannels[i] = trend;
        
        var $channelLink = $('<a href="#" id="channelLink-' + i + '" class="channelLink unseen">' + trend.name + '</a>');

        $($('.topic-channel')[i]).html('');
        $($('.topic-channel')[i]).append($channelLink);

        var f = function(x) {
          return function() {
            switchChannel(x);
          };
        };
        $channelLink.on('click', f(i));
      }
    }
  }
}
function clearNewTopicsBadge() {
  var b = newTopicsCount;
  var g = function() {
    newTopicsCount -= b;
    $('#new-topics-badge').text(newTopicsCount > 0 ? newTopicsCount : '');
  };
  var f = function(x) {
    $('.unseen').removeClass("unseen");
  };
  setTimeout(f, 5000);
  setTimeout(g, 2500);
}
function channelClick() {
  $('.channelLink').removeClass("selected-channel");
  $(this).removeClass("unseen");
  $(this).addClass("selected-channel");
}

function HeatmapMode() {
  heatmap.setMap(map);
  heatmapNeg.setMap(map);
  disableStatesMode();
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

function changeOpacity() {
  heatmap.set('opacity', heatmap.get('opacity') ? null : 0.5);
  heatmapNeg.set('opacity', heatmapNeg.get('opacity') ? null : 0.5);
}

$(document).ready(function() {
  initializeMap();
  initializeHeatmap();
  initializeSocket();
  switchModeCurrent();
  console.log('hey');

  $("#standard_heatmap_btn").on("click", function () {
    HeatmapMode();
  }); 
  
  $("#state_average_btn").on("click", function () {
    switchModeAverage();
  }); 
  
  $("#state_current_btn").on("click", function () {
    switchModeCurrent();
  });
  
  $("#topics-dropdown").click(clearNewTopicsBadge);
  
  $('.dropdown').on('click', '.channelLink', channelClick);
  
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
