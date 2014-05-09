// It's usually a good idea to put everything in a function closure so that variable
// names don't conflict with libraries being used

var hostname = "http://ec2-54-187-28-208.us-west-2.compute.amazonaws.com";
//var hostname = "http://localhost:8080/";

var map, pointArray, pointArrayNeg, heatmap, heatmapNeg;

var data = [];

var dataNeg = [];

var stateAverages = false;
 
function initializeHeatmap() {
  var mapOptions = {
    zoom: 5,
    center: new google.maps.LatLng(41.850033, -87.6500523),
    mapTypeId: google.maps.MapTypeId.SATELLITE
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

}

// Garbage collection: make old points decay
function gc() {
    // Max number of points per array
    var maxPts = 1000;
    var posLen = pointArray.length;
    var negLen = pointArrayNeg.length

    while (posLen != 0) {
        pointArray.remove(0);
        posLen--;
    }

    while (negLen != 0) {
        pointArrayNeg.remove(0);
        neglen--;
    }

}

function initializeSocket() {
    var socket = io.connect(hostname);
    socket.on("newPoint", addPoint);
    socket.on("initialPoints", prePopulate);
    socket.on("trending", changeTrending);
}

function addPoint(data) {
    console.log(data);

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

    addStatePoints(data, stateAverages);
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
  //var data = '[ { "as_of": "2012-08-24T23:25:43Z", "created_at": "2012-08-24T23:24:14Z", "locations": [ { "name": "Worldwide", "woeid": 1 } ], "trends": [ { "events": null, "name": "#GanaPuntosSi", "promoted_content": null, "query": "%23GanaPuntosSi", "url": "http://twitter.com/search/?q=%23GanaPuntosSi" }, { "events": null, "name": "#WordsThatDescribeMe", "promoted_content": null, "query": "%23WordsThatDescribeMe", "url": "http://twitter.com/search/?q=%23WordsThatDescribeMe" }, { "events": null, "name": "#10PersonasQueExtra00f1oMucho", "promoted_content": null, "query": "%2310PersonasQueExtra%C3%B1oMucho", "url": "http://twitter.com/search/?q=%2310PersonasQueExtra%C3%B1oMucho" }, { "events": null, "name": "Apple $1.5", "promoted_content": null, "query": "%22Apple%20$1.5%22", "url": "http://twitter.com/search/?q=%22Apple%20$1.5%22" }, { "events": null, "name": "Zelko", "promoted_content": null, "query": "Zelko", "url": "http://twitter.com/search/?q=Zelko" }, { "events": null, "name": "LWWY", "promoted_content": null, "query": "LWWY", "url": "http://twitter.com/search/?q=LWWY" }, { "events": null, "name": "Lance Armstrong", "promoted_content": null, "query": "%22Lance%20Armstrong%22", "url": "http://twitter.com/search/?q=%22Lance%20Armstrong%22" }, { "events": null, "name": "Gonzo", "promoted_content": null, "query": "Gonzo", "url": "http://twitter.com/search/?q=Gonzo" }, { "events": null, "name": "Premium Rush", "promoted_content": null, "query": "%22Premium%20Rush%22", "url": "http://twitter.com/search/?q=%22Premium%20Rush%22" }, { "events": null, "name": "Sweet Dreams", "promoted_content": null, "query": "%22Sweet%20Dreams%22", "url": "http://twitter.com/search/?q=%22Sweet%20Dreams%22" } ] } ]';
  var obj = JSON.parse(data);
  for (var i = 0; i < 6; i++){
    var trendingName = obj[0].trends[i].name;
    $($(".sidebar-topic-all").children()[i]).text(trendingName.toString());
  }
}

function trendingMode(topic) {
  console.log(topic);
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
	function set_map_height() {
		$(".page-content").css({
			"height": $(window).height() - $(".page-content").offset().top
		});
	}
	$(window).resize(function() {
		set_map_height();
	});
	set_map_height();
});
