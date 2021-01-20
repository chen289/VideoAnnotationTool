var text = [1,2,3,4];
    console.log(text);
    counter = 0;

    $(document).ready(function () {
      var framenum = document.getElementById("frameNumber");
      framenum.addEventListener("keyup", function(event){
        if(event.keyCode == 13) {
           counter = document.getElementById("frameNumber").value;
           if(counter != '') {
              document.getElementById("imageId").src = text[counter];
           }
        }
      });
    });

    function uploadImages() {
      var form = $('#formData')[0];
          var data = new FormData(form);
          $.ajax({
              type: "POST",
              enctype: 'multipart/form-data',
              url: "http://127.0.0.1:8000/upload/",
              data: data,
              processData: false,
              contentType: false,
              cache: false,
              timeout: 600000,
              success: function (data) {
                  console.log("SUCCESS " + data);
                  text = data['context'];
                  displayImages(text);
              },
              error: function (e) {
                  console.log("Error");
              }
          });
    }

    function displayImages(text){
      document.getElementById("imageId").src = text[0];
      document.getElementById("frameNumber").value = counter;
    }

    function jumpToFrame() {
        counter = document.getElementById("frameNumber").value;
        document.getElementById("imageId").src = text[counter];

    }

    function prevFunction() {
      counter--;
      document.getElementById("imageId").src = text[counter];
      if( counter == 0) {
        document.getElementById("prev").disabled = true;
      }
      document.getElementById("frameNumber").value = counter;
    }
    function nextFunction() {
      counter++;
      document.getElementById("imageId").src = text[counter];
      document.getElementById("prev").disabled = false;
        if( counter == text.length - 1) {
        document.getElementById("next").disabled = true;
        }
    document.getElementById("frameNumber").value = counter;
    }

    function drawBoxes() {
        $.ajax({
              type: "GET",
              url: "http://127.0.0.1:8000/drawboxes",
              processData: false,
              contentType: false,
              cache: false,
              timeout: 600000,
              success: function (data) {
                  console.log("SUCCESS " + data);
                  text = data['context'];
                  displayImages(text);
              },
              error: function (e) {
                  console.log("Error");
              }
          });

    }

    function downloadURI(uri, name)
    {
        var link = document.createElement("a");
         link.setAttribute('download', name);
         link.href = uri;
         document.body.appendChild(link);
         link.click();
         link.remove();
    }

    function downloadVideo() {
    $.ajax({
              type: "GET",
              url: "http://127.0.0.1:8000/downloadVideo",
              processData: false,
              contentType: false,
              cache: false,
              timeout: 600000,
              success: function (data) {
                  console.log("SUCCESS " + data);
                  filepath = data['filepath'];
                  filename = data['filename'];
                  downloadURI(filepath, filename)
              },
              error: function (e) {
                  console.log("Error");
              }
          });
    }

    function downloadPostureVideo() {
    $.ajax({
              type: "GET",
              url: "http://127.0.0.1:8000/downloadMergedVideo",
              processData: false,
              contentType: false,
              cache: false,
              timeout: 600000,
              success: function (data) {
                  console.log("SUCCESS " + data);
                  filepath = data['filepath'];
                  filename = data['filename'];
                  downloadURI(filepath, filename)
              },
              error: function (e) {
                  console.log("Error");
              }
          });
    }

    function makePosPoints_BoxesVideo() {

    $.ajax({
              type: "GET",
              url: "http://127.0.0.1:8000/downloadMergedVideo",
              processData: false,
              contentType: false,
              cache: false,
              timeout: 600000,
              success: function (data) {
                  console.log("SUCCESS " + data);
                  filepath = data['filepath'];
                  filename = data['filename'];
                  downloadURI(filepath, filename)
              },
              error: function (e) {
                  console.log("Error");
              }
          });

    }

    function drawPosturePoints() {
      $.ajax({
              type: "GET",
              url: "http://127.0.0.1:8000/drawPosturePoints",
              processData: false,
              contentType: false,
              cache: false,
              timeout: 600000,
              success: function (data) {
                  console.log("SUCCESS " + data);
                  text = data['context'];
                  displayImages(text);
              },
              error: function (e) {
                  console.log("Error");
              }
          });
    }

    function displaySegmentation() {
     $.ajax({
              type: "GET",
              url: "http://127.0.0.1:8000/displaySegmentation",
              processData: false,
              contentType: false,
              cache: false,
              timeout: 600000,
              success: function (data) {
                  console.log("SUCCESS " + data);
                  text = data['context'];
                  displayImages(text);
                  splittext = text.split("/");
                  lengthoftext = splittext.length;
                  seg_frame =  splittext[lengthoftext-1];
                  split_segframe = seg_frame.split(".");
                  document.getElementById("segmentationFrameNumber").value = split_segframe[0];
              },
              error: function (e) {
                  console.log("Error");
              }
          });

    }

    function exportBoundingBoxes() {

      $.ajax({
              type: "GET",
              url: "http://127.0.0.1:8000/exportBoundingBoxes",
              processData: false,
              contentType: false,
              cache: false,
              timeout: 600000,
              success: function (data) {
                  console.log("SUCCESS " + data);
                  filepath = data['filepath'];
                  filename = data['filename'];
                  downloadURI(filepath, filename)
              },
              error: function (e) {
                  console.log("Error");
              }
          });
      }

    function exportPosturePoints() {

      $.ajax({
              type: "GET",
              url: "http://127.0.0.1:8000/exportPosturePoints",
              processData: false,
              contentType: false,
              cache: false,
              timeout: 600000,
              success: function (data) {
                  console.log("SUCCESS " + data);
                  filepath = data['filepath'];
                  filename = data['filename'];
                  downloadURI(filepath, filename)
              },
              error: function (e) {
                  console.log("Error");
              }
          });
      }

    function exportSegmentation() {

        $.ajax({
              type: "GET",
              url: "http://127.0.0.1:8000/exportSegmentation",
              processData: false,
              contentType: false,
              cache: false,
              timeout: 600000,
              success: function (data) {
                  console.log("SUCCESS " + data);
                  filepath = data['filepath'];
                  filename = data['filename'];
                  downloadURI(filepath, filename)
              },
              error: function (e) {
                  console.log("Error");
              }
          });

    }

