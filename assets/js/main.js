/** 
 * Created on May 18, 2014
 * 
 * @author Kristian
 * 
 * Main Javascript file. 
 * All Javascript that is run on every page must go in here.
 */

/*
 * Misc. jQuery code.
 */

$(function () {
	//use local CSS file as fallback if Bootstrap CDN fails
	if ($('#css-check').is(':visible') === true) {
		$('<link rel="stylesheet" type="text/css" href="/static/css/vendor/bootstrap.min.css">').appendTo('head');
	}
});

$(function() {
	if ($('#referralRedirect').length) {		
		ga('send', 'pageview', {
			  'dimension1': referralName,
			  'dimension2': referralSource,
			  'dimension3': referralMedium,
			});
		ga(function() {
			window.location.replace(referralDestination);
		});
    }
});
