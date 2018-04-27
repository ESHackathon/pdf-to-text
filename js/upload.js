// FROM: https://github.com/coligo-io/file-uploader/blob/master/public/javascripts/upload.js
$('#files-to-upload').on('change', function(){
  var files = $(this).get(0).files;
  if (files.length > 0){
    var formData = new FormData();
    for (var i = 0; i < files.length; i++) {
      var file = files[i];
      formData.append('uploads[]', file, file.name);
    }

    $.ajax({
      url: '/pdf-to-txt',
      type: 'POST',
      data: formData,
      processData: false,
      contentType: false,
      success: function(data){
          var references_json = JSON.parse(data);
          $("#step1").css("display", "none");
          $("#step2").css("display", "block");
          $("#txt").html(references_json.txt);
          $("#references").html(references_json.references);
      },
      xhr: function() {
        // create an XMLHttpRequest
        var xhr = new XMLHttpRequest();

        // listen to the 'progress' event
        xhr.upload.addEventListener('progress', function(evt) {

          if (evt.lengthComputable) {
            // calculate the percentage of upload completed
            var percentComplete = evt.loaded / evt.total;
            percentComplete = parseInt(percentComplete * 100);

            // update the Bootstrap progress bar with the new percentage
            $('.progress-bar').text(percentComplete + '%');
            $('.progress-bar').width(percentComplete + '%');

            // once the upload reaches 100%, set the progress bar text to done
            if (percentComplete === 100) {
              $('.progress-bar').html('Done');
            }
          }
        }, false);
        return xhr;
      }
    });
  }
});
