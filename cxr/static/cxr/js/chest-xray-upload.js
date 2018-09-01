$(function () {
  var img_holder = document.getElementById('img_holder'),
    tests = {
      filereader: typeof FileReader != 'undefined',
      formdata: !!window.FormData,
    },
    acceptedTypes = {
      'image/png': true,
      'image/jpeg': true,
      'image/gif': true
    };

  function previewfile(file) {
    if (tests.filereader === true && acceptedTypes[file.type] === true) {
      var reader = new FileReader();
      reader.onload = function (event) {
        var image = new Image();
        image.src = event.target.result;
        image.width = 250; // a fake resize
        img_holder.appendChild(image);
        img_holder.removeChild(img_holder.childNodes[0]);
      };
      document.getElementById('img_name').innerHTML = file.name + ' ';
      document.getElementById('upload_msg').style.display = 'none';
      reader.readAsDataURL(file);
    } else {
      img_holder.innerHTML += '<p>Uploaded ' + file.name + ' ' + (file.size ? (file.size / 1024 | 0) + 'K' : '');
      console.log(file);
    }
  }

  $(".js-upload-photos").click(function () {
    $("#fileupload").click();
  });

  $("#fileupload").fileupload({
    dataType: 'json',
    autoUpload: true,

    add: function (e, data) {
      $('#submit_but').off("click");
      previewfile(data.originalFiles[0])
      debugger;
      $('#submit_but').click(function () {
        data.context = $('<p/>').text('Uploading...').replaceAll($(this));
        debugger;
        data.submit();
      });
    },

    done: function (e, data) {
      debugger;
      alert('Hey hey!');
      if (data.result.is_valid) {
        window.location = data.result.analyse_url;
      }
    },

    fail: function (e, data) {
      alert('Fail!');
    }
  });

});
