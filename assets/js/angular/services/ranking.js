/** 
 * Created on January 4, 2015
 * 
 * @author Kristian
 * 
 * Service to keep track of the currently active ranking.
 */
var rankingService = angular.module('service.ranking', [])

.factory('Rankings', function() {
	
	// The currently active ranking.
    var activeRanking = 'world';
    
    return {
    	setActiveRanking: function(ranking) {
    		activeRanking = ranking;
    	},
        
        getActiveRanking: function() { return activeRanking },
    }
});