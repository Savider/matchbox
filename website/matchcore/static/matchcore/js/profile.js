$("#arrowDown").click(function() {
    if($('#currentProjs').length == 0) {    // no current projs, scrolls to archived
        $('html,body').animate({
        scrollTop: $("#archivedProjs").offset().top},
        'slow');
    }
    else {
        $('html,body').animate({    // scrolls to current projs
        scrollTop: $("#currentProjs").offset().top},
        'slow');
    }
});

$("#circCurrPrj").click(function() {
    $('html,body').animate({
        scrollTop: $("#currentProjs").offset().top},
        'slow');
});

$("#txtCurrPrj").click(function() {
    $('html,body').animate({
        scrollTop: $("#currentProjs").offset().top},
        'slow');
});

$("#circArchPrj").click(function() {
    $('html,body').animate({
        scrollTop: $("#archivedProjs").offset().top},
        'slow');
});

$("#txtArchPrj").click(function() {
    $('html,body').animate({
        scrollTop: $("#archivedProjs").offset().top},
        'slow');
});