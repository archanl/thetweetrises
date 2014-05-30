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

    this.manymaps = {};
    this.initMap("_allpoints");

    this.currentMap = "_allpoints";
    this.hidden = true;

    if (options) {
        if (options.maxPoints) {
            this.maxPoints = options.maxPoints;
        }
    }
}

HeatmapView.prototype.initMap = function(topic) {
    this.manymaps[topic] = {};
    this.manymaps[topic].positivePoints = new google.maps.MVCArray();
    this.manymaps[topic].negativePoints = new google.maps.MVCArray();
    this.manymaps[topic].positiveHeatmap = new google.maps.visualization.HeatmapLayer({
        data: this.manymaps[topic].positivePoints,
        gradient: HEATMAP_GRADIENT_POS,
    });
    this.manymaps[topic].negativeHeatmap = new google.maps.visualization.HeatmapLayer({
        data: this.manymaps[topic].negativePoints,
        gradient: HEATMAP_GRADIENT_NEG,
        opacity: 0.5
    });
}

HeatmapView.prototype.addPoint = function(pnt) {
    var topic = pnt.topic ? pnt.topic : "_allpoints";
    var latlng = new google.maps.LatLng(pnt.latitude, pnt.longitude);

    if (!this.manymaps[topic]) {
        this.initMap(topic);
    }

    if (pnt.sentiment > 0) {
        if (this.manymaps[topic].positivePoints.length > this.maxPoints) {
            this.manymaps[topic].positivePoints.removeAt(0);
        }
        this.manymaps[topic].positivePoints.push(latlng);
    } else {
        if (this.manymaps[topic].negativePoints.length > this.maxPoints) {
            this.manymaps[topic].negativePoints.removeAt(0);
        }
        this.manymaps[topic].negativePoints.push(latlng);
    }
}

HeatmapView.prototype.show = function() {
    this.hidden = false;
    this.manymaps[this.currentMap].positiveHeatmap.setMap(this.map);
    this.manymaps[this.currentMap].negativeHeatmap.setMap(this.map);
}

HeatmapView.prototype.hide = function() {
    this.hidden = true;
    this.manymaps[this.currentMap].positiveHeatmap.setMap(null);
    this.manymaps[this.currentMap].negativeHeatmap.setMap(null);
}

HeatmapView.prototype.switchTopic = function(topic) {
    if (this.hidden) {
        this.currentMap = topic ? topic : "_allpoints";
    } else {
        this.hide();
        this.currentMap = topic ? topic : "_allpoints";
        this.show();
    }
}
