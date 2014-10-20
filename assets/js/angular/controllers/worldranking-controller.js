/** 
 * Created on May 18, 2014
 * 
 * @author Kristian
 * 
 * File for Angular.js controllers.
 */
var xaveeController = angular.module('xavee.worldranking-controller', [])

// Controller for the Ranking page.
.controller('RankingController', ['$scope', '$routeParams', '$location', '$controller', 'WorldRanking', 
                                       function($scope, $routeParams, $location, $controller, WorldRanking) {
	
	angular.extend(this, $controller('TLController', {$scope: $scope}));
	
	var LANG_TO_COUNTRY = { 'en': 'us', 'ja': 'jp' };
	var COUNTRY_TO_INDEX = { 'us': 0, 'jp': 1, 'gb': 2, 'de': 3, 'fr': 4, 'kr': 5, 'au': 6, 'cn': 7, 'ca': 8, 'es': 9, 'it': 10, 'ru': 11, 'nl': 12 };
	
	$scope.platformButton = $routeParams.platform || "iphone";
	$scope.rankingTypeButton = $routeParams.ranking_type || "free";
	$scope.countryButton = $routeParams.country || LANG_TO_COUNTRY[$scope.activeLanguage];
	$scope.activeCategoryID = $routeParams.category || 6014;
	$scope.activeGameCategory = 6014;
	$scope.activeAppCategory = 0;
	$scope.selectedCountry = COUNTRY_TO_INDEX[$scope.countryButton];
	$scope.appType = ($scope.activeCategoryID == 6014 || $scope.activeCategoryID > 6999) ? 1 : 2;
	
	if($scope.appType == 1) {
		$scope.activeGameCategory = $scope.activeCategoryID;
	} else {
		$scope.activeAppCategory = $scope.activeCategoryID;
	}
	
	var updateRanking = function() {
		$scope.pageSize = 20;
		$scope.ranking = WorldRanking.ranking({country:$scope.countryButton, platform: $scope.platformButton, 
											   ranking_type:$scope.rankingTypeButton, category:$scope.activeCategoryID});
	};
	
	var updatePage = function() {
		$location.url("world-rankings/" + $scope.countryButton + "/" + $scope.platformButton + "/" + $scope.rankingTypeButton + "/" + $scope.activeCategoryID);
	};

	$scope.activeGameCategory = 6014;
	updateRanking();
    
    $scope.numberOfPages = function() {
        return Math.ceil($scope.ranking.results[0].ranking.length/$scope.pageSize);
    };

    $scope.loadMore = function() {
    	$scope.pageSize = $scope.pageSize + 20;
    };
	
	$scope.changeRankingType = function(rankingType) {
		$scope.rankingTypeButton = rankingType;
		updatePage();
	};
	
	$scope.changeCountry = function(country, index) {
		$scope.countryButton = country;
		$scope.selectedCountry = index;
		updatePage();
	};
	
	$scope.changeCategory = function(appType, category) {
		$scope.appType = appType;
		$scope.activeCategoryID = category;
		if(appType == 1) {
			$scope.activeGameCategory = category;
		} else {
			$scope.activeAppCategory = category;
		}
		updatePage();
	};
	
//	$rootScope.$watch(function () { return $location.search() }, function (newSearch, oldSearch) {
//		
//		// Check for back/forward button press.
//		if($rootScope.actualSearch === newSearch) {
//			updateEnvironment();
//			updateRanking();
//	    }
//	});
}]);
	