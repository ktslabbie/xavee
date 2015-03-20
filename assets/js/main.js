/** 
 * Created on May 18, 2014
 * 
 * @author Kristian
 * 
 * Main Javascript file. 
 * All plain, non-Angular Javascript that is run on every page must go in here.
 */

// Make Django language changing work with URL rewrites by setting the latest URL and submitting the form manually.
// The function is here to make it possible to switch languages even outside of the Angular environment.
var updateLanguage = function(langCode) {
	$('input[name="next"]').val(window.location.pathname.slice(3));
	$('form[name="setLang' + langCode + '"]').submit();
	return false;
}

/*
 * Misc. jQuery code.
 */
$(function () {
	//use local CSS file as fallback if Bootstrap CDN fails
	if ($('#css-check').is(':visible') === true) {
		$('<link rel="stylesheet" type="text/css" href="/static/css/vendor/bootstrap.min.css">').appendTo('head');
	}
	
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
