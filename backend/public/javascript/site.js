// It's usually a good idea to put everything in a function closure so that variable
// names don't conflict with libraries being used

var hostname = "http://162.243.150.138";
//var hostname = "http://localhost:8080/";

var map, pointArray, pointArrayNeg, heatmap, heatmapNeg;

var data = [];

var dataNeg = [];

var stateAverages = false;
 
function initializeHeatmap() {
  var mapOptions = {
    zoom: 4,
    center: new google.maps.LatLng(39.833333, -98.583333),
    mapTypeId: google.maps.MapTypeId.ROADMAP
  };
  map = new google.maps.Map(document.getElementById('map-canvas'),
      mapOptions);

  pointArray = new google.maps.MVCArray(data);

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
  heatmap.setMap(map);


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
  heatmapNeg.setMap(map);

  // Initialize garbage collection
  window.setInterval(gc, 5000);
  window.setInterval(updateRate, 1000);
}

var numTotalReceivedPoints = 0;
var startTime = new Date().getTime() / 1000;
function updateRate() {
  var elapsed = (new Date().getTime() / 1000) - startTime;
  $('#rateText').text("Rate: " + (numTotalReceivedPoints / elapsed) + " points/second.");
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

function changeTrending(data) {
  console.log('changeTrending(' + data + ')');
  if (data) {
    var obj = JSON.parse(data);
    for (var i = 0; i < 10; i++){
      var trendingName = obj[0].trends[i].name;
      $($(".sidebar-topic-all").children()[i]).html("<a>" + trendingName.toString() + "</a>");
    }
  }
}

function trendingMode(topic) {
  console.log("trendingMode(" + topic + ")");
}

function aboutUs(){
  $("html, body").animate({ scrollTop: $(document).height() }, "slow");
}

function HeatmapMode() {
  heatmap.setMap(map);
  heatmapNeg.setMap(map);
  disableStatesMode();
}

function changeRadiusLarger() {
  heatmap.set('radius', heatmap.get('radius') ? null : 15);
  heatmapNeg.set('radius', heatmapNeg.get('radius') ? null : 15);
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

google.maps.event.addDomListener(window, 'load', initializeHeatmap);
google.maps.event.addDomListener(window, 'load', initializeSocket);

$(function() {

  $("#standard_heatmap_btn").on("click", function () {
    HeatmapMode();
  }); 
  $("#state_average_btn").on("click", function () {
    switchModeAverage();
  }); 
  $("#state_current_btn").on("click", function () {
    switchModeCurrent();
  }); 
  $("#larger_points_btn").on("click", function () {
    changeRadiusLarger();
  }); 
  $("#change_opacity_btn").on("click", function () {
    changeOpacity();
  });
  $("#about_us_btn").on("click", function () {
    aboutUs();
  });
  $(".sidebar-topic").on("click", function () {
    trendingMode($(this).text());
  }); 

  function hours_by_value(value) {
    value = 120 - value;
    hours = Math.floor(value / 60);
    minutes = value - 60 * hours;
    if (hours > 0) {
      if (hours === 1) {
        return String(hours) + " hour " + String(minutes) + " minutes ago";
      }
      return String(hours) + " hours " + String(minutes) + " minutes ago";
    }
    return String(minutes) + " minutes ago";
  }

  $("#time_slider").slider({
      range: true,
      min: 0,
      max: 120,
      step: 1,
      values: [0, 120],
      slide: function (e, ui) {
        var value1 = ui.values[0],
            value2 = ui.values[1],
      time1 = hours_by_value(value1),
      time2 = hours_by_value(value2);
        $("#slider_time_left").text(time1);
        $("#slider_time_right").text(time2);
      }
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
