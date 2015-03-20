/** 
 * Created on January 4, 2015
 * 
 * @author Kristian
 * 
 * Service to keep track of the currently active country.
 */
var countryService = angular.module('service.country', [])

.factory('Countries', function() {
	
	// The currently active country.
    var activeCountry = 'us';
    
    return {
    	setActiveCountry: function(country) {
    		activeCountry = country;
    	},
    	
        getActiveCountry: function() { return activeCountry },
    }
});