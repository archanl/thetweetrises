// Constants

var HEATMAP_GRADIENT_POS = [
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
];
var HEATMAP_GRADIENT_NEG = [
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
];


// HeatMapView definition

var HeatmapView = function(map, options) {
    this.map = map;

    this.maxPoints = 1000;
    // this.garbageCollectorInterval = 5000;

    this.positivePoints = new google.maps.MVCArray();
    this.negativePoints = new google.maps.MVCArray();

    this.positiveHeatmap = new google.maps.visualization.HeatmapLayer({
        data: this.positivePoints,
        gradient: HEATMAP_GRADIENT_POS
    });
    this.negativeHeatmap = new google.maps.visualization.HeatmapLayer({
        data: this.negativePoints,
        gradient: HEATMAP_GRADIENT_NEG
    });

    if (options) {
        if (options.maxPoints) {
            this.maxPoints = options.maxPoints;
        }
    }
}

HeatmapView.prototype.addPoint = function(pnt) {
    var latlng = new google.maps.LatLng(pnt.latitude, pnt.longitude);

    if (pnt.sentiment > 0) {
        if (this.positivePoints.length > this.maxPoints) {
            this.positivePoints.removeAt(0);
        }
        this.positivePoints.push(latlng);
    } else {
        if (this.negativePoints.length > this.maxPoints) {
            this.negativePoints.removeAt(0);
        }
        this.negativePoints.push(latlng);
    }
}

HeatmapView.prototype.show = function() {
    this.positiveHeatmap.setMap(this.map);
    this.negativeHeatmap.setMap(this.map);
}

HeatmapView.prototype.hide = function() {
    this.positiveHeatmap.setMap(null);
    this.negativeHeatmap.setMap(null);
}

/*
HeatmapView.prototype.garbageCollector = function() {
    if (this.positivePoints.length > this.maxPoints) {
        this.positivePoints.splice(0, this.positivePoints.length - this.maxPoints);
    }
    if (this.negativePoints.length > this.maxPoints) {
        this.negativePoints.splice(0, this.negativePoints.length - this.maxPoints);
    }
}

HeatmapView.prototype.startGarbageCollector = function() {
    if (this.garbageCollectorInterval) {
        clearInterval(this.garbageCollectorInterval);
    }
    this.garbageCollectorInterval = setInterval(_.bind(this.garbageCollector, this), 5000);
}

HeatmapView.prototype.stopGarbageCollector = function() {
    if (this.garbageCollectorInterval) {
        clearInterval(this.garbageCollectorInterval);
    }
}
*/