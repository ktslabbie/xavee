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

//$(document).ready(function() {
//	if ($('#referralRedirect').length) {		
//		ga('send', 'pageview', {
//			  'dimension1': referralName,
//			  'dimension2': referralPlatform,
//			  'dimension3': referralSource,
//			  'dimension4': referralMedium,
//			});
//		ga(function() {
//			window.location.replace(referralDestination);
//		});
//    }
//});
