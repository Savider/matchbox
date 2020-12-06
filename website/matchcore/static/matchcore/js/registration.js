const progressBarFull = document.getElementById('progressBarFull');

var canAdvance = false;
var page = 1;

const findProjBtn = document.getElementById("findProjBtn");
const findTeamBtn = document.getElementById("findTeamBtn");
const notSureBtn1 = document.getElementById("notSureBtn1");
const newcomerBtn = document.getElementById("newcomerBtn");
const adeptBtn = document.getElementById("adeptBtn");
const proBtn = document.getElementById("proBtn");
const notSureBtn2 = document.getElementById("notSureBtn2");

const nextBtn = document.getElementById("nextBtn");
const nextBtnSubmit = document.getElementById("nextBtnSubmit");

const options1 = [findProjBtn, findTeamBtn, notSureBtn1];
const options2 = [newcomerBtn, adeptBtn, proBtn, notSureBtn2];

for (const btn of options1) {
	btn.onclick = selectOption.bind(this, [btn, options1]);
}
for (const btn of options2) {
	btn.onclick = selectOption.bind(this, [btn, options2]);
}
nextBtn.onclick = clickNext.bind(this);


function selectOption(args, event) {
	const button = args[0];
	const options = args[1];
	for (const btn of options) {
		btn.style.backgroundColor = '#221122';
		btn.style.color = '#D33F49';
	}
	button.style.backgroundColor = '#D33F49';
	button.style.color = '#FFFFFF';
	nextBtn.classList.add("active");
	canAdvance = true;

	// spaghetti code below (even more than usual!)
	if (button === findProjBtn)
		$('#id_objective_tag').val('Joiner');
	else if (button === findTeamBtn)
		$('#id_objective_tag').val('Creator');
	else if (button === notSureBtn1)
		$('#id_objective_tag').val('');
	else if (button === newcomerBtn)
		$('#id_expertise_tag').val('Newcomer');
	else if (button === adeptBtn)
		$('#id_expertise_tag').val('Adept');
	else if (button === proBtn)
		$('#id_expertise_tag').val('Pro');
	else if (button === notSureBtn2)
		$('#id_expertise_tag').val('');

	if (button === findProjBtn) {
		$(".imgwhite:not(#projImgWhite)").fadeOut(230, function(){
			$('#projImgWhite').fadeIn(230);
			});
	}
	else if (button === findTeamBtn) {
		$(".imgwhite:not(#teamImgWhite)").fadeOut(230, function(){
			$('#teamImgWhite').fadeIn(230);
			});
	}
	else if (button === newcomerBtn) {
		$(".imgwhite:not(#newcomerImgWhite)").fadeOut(230, function(){
			$('#newcomerImgWhite').fadeIn(230);
			});
	}
	else if (button === adeptBtn) {
		$(".imgwhite:not(#adeptImgWhite)").fadeOut(230, function(){
			$('#adeptImgWhite').fadeIn(230);
			});
	}
	else if (button === proBtn) {
		$(".imgwhite:not(#proImgWhite)").fadeOut(230, function(){
			$('#proImgWhite').fadeIn(230);
			});
	}
}

function clickNext(event) {
	if (canAdvance) {
		changePage();
		canAdvance = false;
		nextBtn.classList.remove("active");
	}
}

function changePage() {
	if (page == 1) {
		$('#regHeader').fadeOut(300, function(){
			$('#regHeader').text("What would describe you?").fadeIn(300);
		});
		$('#findProjBtn').fadeOut(300, function(){
			$(this).remove();
			$('#newcomerBtn').fadeIn(300);
			});
		$('#findTeamBtn').fadeOut(300, function(){
			$(this).remove();
			$('#adeptBtn').fadeIn(300);
			$('#proBtn').fadeIn(300);
		});
		$('#notSureBtn1').fadeOut(300, function(){
			$(this).remove();
			$('#notSureBtn2').fadeIn(300);
		});
		$('#progressBarFull').animate({'width': '66%'});
	}
	else {
		$('#regPage12').fadeOut(300, function(){
			$(this).remove();
			$('#regPage3').fadeIn(300);
		});
		$('#nextBtn').fadeOut(300, function(){
			$(this).remove();
			$('#nextBtnSubmit').fadeIn(300);
		});
		$('#progressBarFull').animate({'width': '100%'});
		$('#progressBarFull').animate({'width': '+=2px'});
		setTimeout(function() {
			$('#progressBar').animate({'background-color': '#D33F49'}, 100);	
		}, 400);
	}
	page++;
}


/*------------------------------*/


var $fields = $('.r-req');

$fields.on('keyup change', function() {
	if (allFilled($fields)) {
	   	nextBtnSubmit.classList.add("active");
	}
});

function allFilled($fields) {
	return $fields.filter(function() {
	  return this.value === ''; 
	}).length == 0;
}

$("#register-picture").attr("onclick","uploadImg()");
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
      $('#register-picture').attr('src', e.target.result);
    }
    reader.readAsDataURL(input.files[0]); // convert to base64 string
  }
}