function TweetRisesApp(options) {
    this.map = new google.maps.Map(document.getElementById(options.mapCanvasId), options.mapOptions);

    this.heatmap = new HeatmapView(this.map);
    // this.heatmap.startGarbageCollector(); // functionality now removed
    this.statesmap = new StatemapView(this.map);

    this.topics = [];
    this.currentView = this.heatmap;

    // Point count data
    this.numTotalReceivedPoints = 0;
    this.updateRateRate = 2; // seconds
    this.lastZero = false;
    this.zeroSince = Math.floor((new Date()).getTime() / 1000);
    this.timeOutAppended = false;

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

    if (this.numTotalReceivedPoints > 0) {
        this.lastZero = false;
        if (this.timeOutAppended) {
            $('#server-no-points-alert').remove();
        }
    } else {
        if (this.lastZero) {
            var now = Math.floor((new Date()).getTime() / 1000);
            if (!this.timeOutAppended && now - this.zeroSince > 10) {
                $('#error-messages').append(
                    '<div id="server-no-points-alert" class="alert alert-warning alert-dismissable">' +
                        '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' +
                        '<strong>Something is wrong!</strong> The server is not be sending any points.' +
                    '</div>'
                );

                this.timeOutAppended = true;
            }
        } else {
            this.zeroSince = Math.floor((new Date()).getTime() / 1000);
        }

        this.lastZero = true;
    }
    this.numTotalReceivedPoints = 0;
};

TweetRisesApp.prototype.switchView = function(view) {
    if (view === 'heatmap') {
        this.currentView.hide();
        this.currentView = this.heatmap;
        this.currentView.show();
    } else if (view === 'states') {
        this.currentView.hide();
        this.currentView = this.statesmap;
        this.currentView.show();
    }
};

TweetRisesApp.prototype.switchTopic = function(topic) {
    this.heatmap.switchTopic(topic);
    if (topic){
        this.statesmap.switchTopic(topic);
    }
    else{
        this.statesmap.showAll();
    }
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
    this.statesmap.addPoint(pnt);
    this.statesmap.storeAllStatePoints(pnt, 250);
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
