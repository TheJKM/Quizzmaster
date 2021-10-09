let questionState = {
  getString: function(input) {
    switch(input) {
      case 0:
        return "Vor Vorbereitung";
      case 1:
        return "Dummys werden verschickt";
      case 2:
        return "Vor Fragestellung";
      case 3:
        return "Frage gestellt";
      case 4:
        return "Warten auf Auswertung";
      case 5:
        return "In Auswertung";
      case 6:
        return "Warten auf Scoreboard-Freigabe";
      case 7:
        return "Auf Scoreboard freigegeben";
    }
  }
}

export default questionState;
