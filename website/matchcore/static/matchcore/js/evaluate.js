$('.score-button').on('click', function() {
	let score = $(this).text();
	let form_id = $(this).data('id')
	$('#id_form-' + form_id + '-contribution').val(score);

	// reset all others
	$('.score-button[data-id="' + form_id + '"]').not(this).css('background-color', '#FFFFFF');
	$('.score-button[data-id="' + form_id + '"]').not(this).css('color', '#D33F49');

	// change this one's color
	$(this).css('background-color', '#D33F49');
	$(this).css('color', '#FFFFFF');
});