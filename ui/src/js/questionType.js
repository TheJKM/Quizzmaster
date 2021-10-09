let questionType = {
  getString: function(input) {
    switch(input) {
      case 0:
        return "Freitext";
      case 1:
        return "Multiple Choice";
      case 2:
        return "Wahr / Falsch";
    }
  }
}

export default questionType;
