$("#overlayClick").attr("onclick","uploadImg()");
$("#id_img").change(function() {
  readURL(this);
});

function uploadImg(){
    document.getElementById("id_img").click();
}

function readURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();
    reader.onload = function(e) {
      $('#userImg').attr('src', e.target.result);
    }
    reader.readAsDataURL(input.files[0]); // convert to base64 string
  }
}