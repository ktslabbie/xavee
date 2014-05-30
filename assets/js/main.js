/** 
 * Main Javascript file. 
 * All Javascript that is run on every page must go in here.
 * 
 * @author Kristian
 */

$(document).ready(function() {

	if ($('#referralRedirect').length) {
		var paramString = 'utm_campaign=' + referralName +  '&utm_source=' + referralSource + '&utm_medium=' + referralMedium;
		alert(paramString);
		
		_gaq.push(['_trackPageview', referralDestination + '?' + paramString]);
		
		//_gaq.push( ['_set', 'campaignParams', 
		//            'utm_campaign=' + referralName +  '&utm_source=' + referralSource + '&utm_medium=' + referralMedium] );
		//_gaq.push(['_setAccount', 'UA-51423008-1']);
        //_gaq.push(['_trackPageview']);
		//window.location.replace(referralDestination);
    }
	
});
