$(function() {
	var notifReqInterval = 1 * 1000;
	var fetchNotifs = function() {
		$.ajax({
			type: "GET",
			url: "/notifs_num"
		}).done(function(response) {
			if (response.num_notifs > 0)
				$('#notifBadge').text(response.num_notifs);
			else
				$('#notifBadge').empty();
		}).fail(function() {
		}).always(function() {
			setTimeout(fetchNotifs, notifReqInterval);
		});
	}
	fetchNotifs();
});