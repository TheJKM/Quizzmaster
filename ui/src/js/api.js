/*
 API JS for CoWhere.
 © 2020 - 2021 Johannes Kreutz. Alle Rechte vorbehalten.
 */

import my from './my.js';

let api = {
  send: function(url, type, data, isPlain = false) {
    return new Promise(function(resolve, reject) {
      let request = new XMLHttpRequest;
      request.addEventListener("load", function(event) {
        if (event.target.status >= 200 && event.target.status < 300) {
          resolve(event.target.responseText, event.target.status);
        } else {
          this.processError(event.target.status, event.target.responseText);
        }
      }.bind(this));
      request.addEventListener("error", function(event) {
        this.processError(event.target.status, event.target.responseText);
      }.bind(this));
      request.open(type, url, true);
      if (isPlain) {
        request.send(data);
      } else {
        let requestData = null;
        requestData = new FormData();
        for (let key in data) {
          requestData.append(key, data[key])
        }
        request.send(requestData);
      }
    }.bind(this));
  },
  processError: function(code, data) {
    my.app.preloader.hide();
    my.app.dialog.close();
    if (code == 404) {
      this.fire404Error();
    } else if (code == 403) {
      this.fire403Error();
    } else if (code == 401) {
      if (my.ls == null) {
        my.ls = my.app.loginScreen.create({
          el: "#my-login-screen",
        });
      }
      console.log(my.ls);
      my.ls.open();
    } else if (code == 400 && data == "ERR_NOT_NUMERIC") {
      this.fireNumericError();
    } else {
      this.fallbackError();
    }
  },
  fire404Error: function() {
    my.app.dialog.alert("Die angeforderte Ressource konnte nicht gefunden werden.");
  },
  fire403Error: function() {
    my.app.dialog.alert("Zugriff nicht erlaubt.");
  },
  fallbackError: function() {
    my.app.dialog.alert("Es ist ein Fehler aufgetreten.");
  },
  fireNumericError: function() {
    my.app.dialog.alert("Einige Punktstände konnten nicht als Zahl interpretiert werden. Bitte die Punkte überprüfen.");
  }
}

export default api;
