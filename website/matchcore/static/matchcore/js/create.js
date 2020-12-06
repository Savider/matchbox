$('.period select').val(2).trigger('change');

$('.complexity-choice').on('click', function() {
	$('#id_complexity').val($(this).data('optnval'));
	$('#selectedComplexity').text($(this).text());
})

$('.theme-choice').on('click', function() {
	$('#id_theme').val($(this).data('optnval'));
	$('#selectedTheme').text($(this).text());
})

$('.technology-choice').on('click', function() {
	$('#id_technology').val($(this).data('optnval'));
	$('#selectedTechnology').text($(this).text());
})

$('.language-choice').on('click', function() {
	$('#id_language').val($(this).data('optnval'));
	$('#selectedLanguage').text($(this).text());
})

$("#projImg").attr("onclick","uploadImg()");
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
      $('#projImg').attr('src', e.target.result);
    }
    reader.readAsDataURL(input.files[0]); // convert to base64 string
  }
}