/** 
 * Main Javascript file. 
 * All Javascript that is run on every page must go in here.
 * 
 * @author Kristian
 */

$(document).ready(function() {

	if ($('#referralRedirect').length) {
		
		_gaq.push( ['_set', 'campaignParams', 
		            'utm_campaign=' + referralName +  '&utm_source=' + referralSource + '&utm_medium=' + referralMedium] );
		window.location.replace(referralDestination);
    }
	
});
