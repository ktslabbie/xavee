/** 
 * Created on May 18, 2014
 * 
 * @author Kristian
 * 
 * Service to transfer active app/store IDs across the application.
 */
var appstoreIDService = angular.module('service.appstore-id', [])

.factory('AppstoreID', function() {
    var itunesID = 0;
    var country = CONSTS.defaults.country;
    
    return {
    	setAppstoreID: function(id, cntry) {
    		itunesID = id;
    		country = cntry;
    	},
    	
        getAppstoreID: function() {
            return itunesID;
        },
    	
    	getAppstoreCountry: function() {
            return country;
        }
    }
});