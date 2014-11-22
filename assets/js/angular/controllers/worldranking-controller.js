/** 
 * Created on May 18, 2014
 * 
 * @author Kristian
 * 
 * File for Angular.js controllers.
 */
var xaveeController = angular.module('xavee.worldranking-controller', [])

// Controller for the Ranking page.
.controller('RankingController', ['$scope', '$routeParams', '$location', '$controller', '$timeout', 'StoreID', 'WorldRanking', 
                                       function($scope, $routeParams, $location, $controller, $timeout, StoreID, WorldRanking) {
	
	angular.extend(this, $controller('BaseController', {$scope: $scope}));
	angular.extend(this, $controller('TLController', {$scope: $scope}));
	
	$scope.platformButton = $routeParams.platform || "iphone";
	$scope.rankingTypeButton = $routeParams.ranking_type || "free";
	$scope.activeCountry = $routeParams.country || LANG_TO_COUNTRY[$scope.activeLanguage];
	$scope.activeCategoryID = $routeParams.category || 6014;
	$scope.activeGameCategory = 6014;
	$scope.activeAppCategory = 0;
	$scope.selectedCountry = COUNTRY_TO_INDEX[$scope.activeCountry];
	$scope.appType = ($scope.activeCategoryID == 6014 || $scope.activeCategoryID > 6999) ? 1 : 2;
	
	if($scope.appType == 1) {
		$scope.activeGameCategory = $scope.activeCategoryID;
	} else {
		$scope.activeAppCategory = $scope.activeCategoryID;
	}
	
	var updateRanking = function() {
		$scope.pageSize = 15;
		WorldRanking.ranking({country:$scope.activeCountry, platform: $scope.platformButton, 
							  ranking_type:$scope.rankingTypeButton, category:$scope.activeCategoryID}, function(data) {
												   
			var ranking = data.ranking;
			data.ranking = [];
			$scope.ranking = data;
			var time = 0;
			
			_.each(ranking, function(entry) {
				$timeout(function () {
					$scope.ranking.ranking.push(entry);
				}, time); 
				time += 30;
			});
		});
	};
	
	var updatePage = function() {
		$location.url("world-rankings/" + $scope.activeCountry + "/" + $scope.platformButton + "/" + $scope.rankingTypeButton + "/" + $scope.activeCategoryID);
	};

	$scope.activeGameCategory = 6014;
	updateRanking();
    
    $scope.numberOfPages = function() {
        return Math.ceil($scope.ranking.results[0].ranking.length/$scope.pageSize);
    };

    $scope.loadMore = function() {
    	$scope.pageSize = $scope.pageSize + 15;
    };
	
	$scope.changeRankingType = function(rankingType) {
		$scope.rankingTypeButton = rankingType;
		updatePage();
	};
	
	$scope.changeCountry = function(country, index) {
		$scope.activeCountry = country;
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
	
	$scope.setAppstoreID = function(id, country) {
		StoreID.setAppstoreID(id, country);
	}
}]);
	