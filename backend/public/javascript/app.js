function TweetRisesApp(options) {
    this.map = new google.maps.Map(document.getElementById(options.mapCanvasId), options.mapOptions);

    this.heatmap = new HeatmapView(this.map);
    // this.heatmap.startGarbageCollector(); // functionality now removed
    // this.statesmap = new StatesMapView(this.map);

    this.topics = [];
    this.currentView = this.heatmap;

    // Point count data
    this.numTotalReceivedPoints = 0;
    this.updateRateRate = 2; // seconds

    // Event handlers
    this.newTopicHandler = options.newTopicHandler;
    this.newRateHandler = options.newRateHandler;
}

TweetRisesApp.prototype.connect = function(hostname) {
    if ('undefined' !== typeof io) {
        var socket = io.connect(hostname);

        // Initialize rate counter
        setInterval(_.bind(this.updateRate, this), this.updateRateRate * 1000);

        socket.on("newPoint", _.bind(this.addPoint, this));
        socket.on("newPoints", _.bind(this.addPoints, this));

        this.currentView.show();
    } else {
        $('#error-messages').append('<div class="alert alert-danger">Error! Cannot connect to server. Please try again.</div>');
        return false;
    }
};

TweetRisesApp.prototype.updateRate = function() {
    this.newRateHandler(Math.floor(this.numTotalReceivedPoints / this.updateRateRate));
    this.numTotalReceivedPoints = 0;
};

TweetRisesApp.prototype.switchView = function(view) {
    if (view === 'heatmap') {
        this.currentView.hide();
        this.currentView = this.heatmap;
        this.currentView.show();
    } else if (view === 'states') {
        this.currentView.hide();
        // TODO
    }
};

TweetRisesApp.prototype.switchTopic = function(topic) {
    console.log('switching to topic: ' + topic);
};

TweetRisesApp.prototype.addPoint = function(data) {
    if (!data) {
        return;
    }

    this.numTotalReceivedPoints++;

    var pnt = JSON.parse(data);

    if (pnt.topic) {
        var topic = decodeURIComponent(pnt.topic);

        console.log("point has topic: " + topic);

        if (_.indexOf(this.topics, topic) === -1) {
            var that = this;

            this.topics.push(topic);

            this.newTopicHandler(topic, function() {
                that.switchTopic(topic);
            });
        }
    }

    this.heatmap.addPoint(pnt);
    // this.statesmap.addPoint(pnt);
};

TweetRisesApp.prototype.addPoints = function(data) {
    if (!data) {
        return;
    }

    var pnts = data;

    for (var i = 0; i < pnts.length; i++) {
        this.addPoint(pnts[i]);
    }
};
