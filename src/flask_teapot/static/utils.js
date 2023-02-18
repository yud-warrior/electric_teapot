async function promiseTime() {
    let url = "/time";
    let response = await fetch(url);
    let msg = await response.json();
    return msg.time;
  }

  function getTime() {
    promiseTime().then(
      function(value) {document.getElementById("time").innerHTML = value;},
      function(error) {document.getElementById("time").innerHTML = error;}
    );
  }

  async function promiseState() {
    let url = "/state";
    let response = await fetch(url);
    let msg = await response.json();
    return msg.state;
  }

  function getState() {
    promiseState().then(
      function(value) {document.getElementById("state").innerHTML = value;},
      function(error) {document.getElementById("state").innerHTML = error;}
    );
  }

  async function promiseRelVolume() {
    let url = "/relvolume";
    let response = await fetch(url);
    let msg = await response.json();
    return msg.relvolume;
  }

  function getRelVolume() {
    promiseRelVolume().then(
      function(value) {document.getElementById("relativevolume").innerHTML = value;},
      function(error) {document.getElementById("relativevolume").innerHTML = error;}
    );
  }

  async function promiseTemperature() {
    let url = "/temperature";
    let response = await fetch(url);
    let msg = await response.json();
    return msg.temperature;
  }

  function getTemperature() {
    promiseTemperature().then(
      function(value) {document.getElementById("temperature").innerHTML = value;},
      function(error) {document.getElementById("temperature").innerHTML = error;}
    );
  }

  async function promiseTurnOn() {
    let url = "/turnon";
    let response = await fetch(url);
    let msg = await response.json();
    return msg.message;
  }

  function TurnOn() {
    promiseTurnOn().then(
      function(value) {document.getElementById("turnon msg").innerHTML = value;},
      function(error) {document.getElementById("turnon msg").innerHTML = error;}
    );
  }

  async function promiseTurnOff() {
    let url = "/turnoff";
    let response = await fetch(url);
    let msg = await response.json();
    return msg.message;
  }

  function TurnOff() {
    promiseTurnOff().then(
      function(value) {document.getElementById("turnoff msg").innerHTML = value;},
      function(error) {document.getElementById("turnoff msg").innerHTML = error;}
    );
  }