/** 
 * Created on May 18, 2014
 * 
 * @author Kristian
 * 
 * Main Javascript file. 
 * All Javascript that is run on every page must go in here.
 */

$(document).ready(function() {

	if ($('#referralRedirect').length) {		
		ga('send', 'pageview', {
			  'dimension1': referralName,
			  'dimension2': referralPlatform,
			  'dimension3': referralSource,
			  'dimension4': referralMedium,
			});
		ga(function() {
		    setTimeout(function() {
		        window.location.replace(referralDestination);
		    }, 200)});
    }
});
