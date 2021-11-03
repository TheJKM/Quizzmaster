let questionType = {
  getString: function(input) {
    switch(input) {
      case 0:
        return "Freitext";
      case 1:
        return "Multiple Choice";
      case 2:
        return "Wahr / Falsch";
      case 3:
        return "Custom Automatisch";
      case 4:
        return "Custom Manuell";
      case 5:
        return "Custom Automatisch MC";
    }
  }
}

export default questionType;
