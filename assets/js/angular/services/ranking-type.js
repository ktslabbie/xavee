/** 
 * Created on January 4, 2015
 * 
 * @author Kristian
 * 
 * Service to keep track of the currently active ranking type.
 */
var rankingTypeService = angular.module('service.ranking-type', [])

.factory('RankingTypes', function() {
	
	// The currently active ranking type.
    var activeRankingType = CONSTS.defaults.rankingType;
    var activeRankingTypeList = CONSTS.rankingTypeLists[CONSTS.defaults.rankingTypeList];
    
    return {
    	setActiveRankingType: function(rankingType) {
    		activeRankingType = rankingType;
    	},
    	
    	setActiveRankingTypeList: function(rankingTypeList) {
    		activeRankingTypeList = CONSTS.rankingTypeLists[rankingTypeList];
    	},
        
        getActiveRankingType: function() { return activeRankingType },
        getActiveRankingTypeList: function() { return activeRankingTypeList },
    }
});