function WSSHClient() {
};

WSSHClient.prototype._generateEndpoint = function (options) {
    if (window.location.protocol == 'https:') {
        var protocol = 'wss://';
    } else {
        var protocol = 'ws://';
    }
    var endpoint = protocol + window.location.host + '/webssh/' + encodeURIComponent(options.dest_id) + '/';
    console.log(endpoint);
    return endpoint;
};

WSSHClient.prototype.connect = function (options) {
    var endpoint = this._generateEndpoint(options);


    if (window.WebSocket) {
        this._connection = new WebSocket(endpoint);
    }
    else if (window.MozWebSocket) {
        this._connection = MozWebSocket(endpoint);
    }
    else {
        options.onError('WebSocket Not Supported');
        return;
    }

    this._connection.onerror = function (evt) {
        options.onError(evt);
    };

    this._connection.onopen = function () {
        options.onConnect();
    };

    this._connection.onmessage = function (evt) {
        var data = evt.data.toString();
        options.onData(data);
    };


    this._connection.onclose = function (evt) {
        options.onClose(evt);
    };
};

WSSHClient.prototype.send = function (data) {
    this._connection.send(JSON.stringify(data));
};

WSSHClient.prototype.sendInitData = function (options) {
    // var data = {
    //     hostname: options.host,
    //     port: options.port,
    //     username: options.username,
    //     ispwd: options.ispwd,
    //     secret: options.secret
    // };
    // this._connection.send(JSON.stringify({"tp": "init", "data": data}))
    console.log(options);
    this._connection.send(JSON.stringify(options))
};

WSSHClient.prototype.sendClientData = function (data) {
    //this._connection.send(JSON.stringify({"tp": "client", "data": data}))
    this._connection.send(JSON.stringify(data))
};

//var client = new WSSHClient();