/* 

Funicular.js - JS Library
https://github.com/adeniszczyc/Funicular.js
Andrew Deniszczyc

Override Funicular functions as shown below:

Funicular.onHandsMove = function(hands) {
  // CUSTOM CODE
}
*/

/*==========  Config Settings  ==========*/

var port = 8888

/*==========  Funicular.js Declaration  ==========*/

window.Funicular = {

  // Connected to websocket server
  onSocketOpen: function() {},

  // Disconnected from websocket server
  onSocketClose: function() {},
  onSocketMessage: function() {},

  // Detected wave gesture
  // x, y, z are coordinates of gesture
  onGestureWave: function(x, y, z) {},

  // Detected click gesture
  // x, y, z are coordinates of gesture
  onGestureClick: function(x, y, z) {},

  // Hand detected, now tracking
  // hand: {id, x, y, z}
  onHandsRegister: function(hand) {},

  // Hand moved.
  // hands: [{id, x, y, z}]
  onHandsMove: function(hands) {},

  // Hand tracking lost hand, no longer tracking
  // hand: {id}
  onHandsUnregister: function(hand) {}
};

Funicular = window.Funicular;

/*==========  Helper Functions  ==========*/

// Object to Array conversion
// http://stackoverflow.com/questions/4607991/javascript-transform-object-into-array
function objectToArray(obj) {
  return Object.keys(obj).map(function (key) { return obj[key]; });
}

/*==========  Websocket Connection ==========*/

var url = "ws://localhost:" + port + "/ws"
var ws = new WebSocket(url);

ws.onerror = function(e) {
  console.log("Make sure the websocket server is running through Python.")
};

ws.onopen = function() {
   Funicular.onSocketOpen();
};

ws.onclose = function() {
   Funicular.onSocketClose();
};

ws.onmessage = function (evt) {
  Funicular.onSocketMessage()
  var data = JSON.parse(evt.data);
  var type = data.type;

  delete data.type;

  if (type == "gesture") {

    x = data.end_point[0];
    y = data.end_point[1];
    z = data.end_point[2];

    switch (data.gesture) {
      case "Wave": Funicular.onGestureWave(x, y, z);
      case "Click": Funicular.onGestureClick(x, y, z);
      default: break;
    }
  }

  else if (type == "register") {
    Funicular.onHandsRegister(data)
  }

  else if (type == "unregister") {
    Funicular.onHandsUnregister(data)
  }

  else if (type == "hands") {
    Funicular.onHandsMove(objectToArray(data.hands))
  }
};
