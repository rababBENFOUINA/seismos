function ajouterLignedate(table, nbCellulesselect, nbCellulesText,nbCellulesDate, attname , liste) {
  // Récupère le corps du tableau
  var tableBody = table.querySelector("tbody");

  // Crée une nouvelle ligne
  var newRow = document.createElement("tr");

    // Crée les cellules pour la nouvelle ligne
    for (var i = 0; i < nbCellulesselect; i++) {
          // Crée une cellule pour le champ de sélection
      var selectCell = document.createElement("td");

      // Crée un élément de sélection
      var selectInput = document.createElement("select");
      selectInput.classList.add("form-select");
      selectInput.classList.add("table-input-costum");
      selectInput.classList.add("text-dark")

      var options=liste[i]
     // Ajoute des options à l'élément de sélection
      for (var j = 0; j < options.length; j++) {
        var option = document.createElement("option");
        option.text = options[j];
        selectInput.add(option);
      }

      // Ajoute un attribut "name" à l'élément de sélection
      selectInput.setAttribute("name", attname);
      

      // Ajoute l'élément de sélection à la cellule
      selectCell.appendChild(selectInput);

      // Ajoute la cellule de sélection à la nouvelle ligne
      newRow.appendChild(selectCell);

  }

  // Crée les cellules pour la nouvelle ligne
  for (var i = 0; i < nbCellulesText; i++) {
      var cell = document.createElement("td");

      // Crée un champ de saisie de texte pour chaque cellule
      var input = document.createElement("input");
      input.setAttribute("type", "text");
      input.classList.add("form-control");
      input.classList.add("table-input-costum");
      input.classList.add("text-dark")

      // Ajoute un attribut "name" à l'élément "input"
      input.setAttribute("name", attname);
      input.setAttribute("autocomplete", "off");

      // Ajoute le champ de saisie de texte à la cellule
      cell.appendChild(input);

      // Ajoute la cellule à la nouvelle ligne
      newRow.appendChild(cell);
  }

  // Crée les cellules pour la nouvelle ligne
  for (var i = 0; i < nbCellulesDate; i++) {
    // Crée une cellule pour le champ de saisie de date
      var dateCell = document.createElement("td");

      // Crée un champ de saisie de date
      var dateInput = document.createElement("input");
      dateInput.setAttribute("type", "date");
      dateInput.classList.add("form-control");
      dateInput.classList.add("table-input-costum");
      dateInput.classList.add("text-dark");

      // Ajoute un attribut "name" à l'élément "input"
      dateInput.setAttribute("name", attname);

      // Ajoute le champ de saisie de date à la cellule
      dateCell.appendChild(dateInput);

      // Ajoute la cellule de date à la nouvelle ligne
      newRow.appendChild(dateCell);
}

  

  // Ajoute la nouvelle ligne au corps du tableau
  tableBody.appendChild(newRow);
}



/**************************************************************************************** */
  
  
function ajouterLigne(table, nbCellulesselect, nbCellulesText,nbCellulesDate, attname , liste) {
  // Récupère le corps du tableau
  var tableBody = table.querySelector("tbody");

  // Crée une nouvelle ligne
  var newRow = document.createElement("tr");


  // Crée les cellules pour la nouvelle ligne
  for (var i = 0; i < nbCellulesselect; i++) {
    // Crée une cellule pour le champ de sélection
    var selectCell = document.createElement("td");

    // Crée un élément de sélection
    var selectInput = document.createElement("select");
    selectInput.classList.add("form-select");
    selectInput.classList.add("table-input-costum");
    selectInput.classList.add("text-dark")

    var options=liste[i]
    // Ajoute des options à l'élément de sélection
    for (var j = 0; j < options.length; j++) {
      var option = document.createElement("option");
      option.text = options[j];
      selectInput.add(option);
    }

    // Ajoute un attribut "name" à l'élément de sélection
    selectInput.setAttribute("name", attname);

    // Ajoute l'élément de sélection à la cellule
    selectCell.appendChild(selectInput);

    // Ajoute la cellule de sélection à la nouvelle ligne
    newRow.appendChild(selectCell);

    }


  // Crée les cellules pour la nouvelle ligne
  for (var i = 0; i < nbCellulesText; i++) {
    var cell = document.createElement("td");

    // Crée un champ de saisie de texte pour chaque cellule
    var input = document.createElement("input");
    input.setAttribute("type", "text");
    input.classList.add("form-control");
    input.classList.add("table-input-costum");

    // Ajoute un attribut "name" à l'élément "input"
    input.setAttribute("name", attname);
    input.setAttribute("autocomplete", "off");

    // Ajoute le champ de saisie de texte à la cellule
    cell.appendChild(input);

    // Ajoute la cellule à la nouvelle ligne
    newRow.appendChild(cell);

    if (i === 0) {
      cell.style.display = "none";
    }
  }

  // Crée les cellules pour la nouvelle ligne
  for (var i = 0; i < nbCellulesDate; i++) {
    // Crée une cellule pour le champ de saisie de date
    var dateCell = document.createElement("td");

    // Crée un champ de saisie de date
    var dateInput = document.createElement("input");
    dateInput.setAttribute("type", "date");
    dateInput.classList.add("form-control");
    dateInput.classList.add("table-input-costum");

    // Ajoute un attribut "name" à l'élément "input"
    dateInput.setAttribute("name", attname);

    // Ajoute le champ de saisie de date à la cellule
    dateCell.appendChild(dateInput);

    // Ajoute la cellule de date à la nouvelle ligne
    newRow.appendChild(dateCell);

    // Rend la première cellule invisible
    
  }
  
// Ajoute la nouvelle ligne au corps du tableau
tableBody.appendChild(newRow);
}

/**************************************************************************************************/
function replaceImage() {
  var selectedImage = document.querySelector('input[type=file]').files[0];
  var imagePreview = document.getElementById('profil-img');
  imagePreview.src = URL.createObjectURL(selectedImage);
}

/************************************************************************************************ */
/*function redirect() {
  // Récupérer la valeur de l'input avec l'ID "inputId"
  const inputValue = document.getElementById("inputId").value;

  // Rediriger la page vers une nouvelle URL en utilisant la méthode "window.location.replace"
  window.location.replace("http://www.example.com/page/" + inputValue);
}*/ 



  