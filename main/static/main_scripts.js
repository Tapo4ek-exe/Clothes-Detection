function previewFile() {
    var preview = document.querySelector('#preview-image');
    var file    = document.querySelector('input[type=file]').files[0];
    var reader  = new FileReader();
  
    reader.onloadend = function () {
      preview.src = reader.result;
    }
  
    if (file) {
      reader.readAsDataURL(file);
    } else {
      preview.src = "";
    }
  }

  function closeHelp() {
    document.location.href = "#";
  }

  function loadAnimation(mode) {
    $('#loadModalCenter').modal({backdrop:'static', keyboard:false});
    if (mode)
      $('#loadModalCenter').modal('show');
    else
      $('#loadModalCenter').modal('hide');
  }

  