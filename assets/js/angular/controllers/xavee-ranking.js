/** 
 * Created on May 18, 2014
 * 
 * @author Kristian
 * 
 * File for Angular.js controllers.
 */
var xrCtrl = angular.module('ctrl.xavee-ranking', [])

// Controller for the Ranking page.
.controller('XaveeRankingCtrl', ['$scope', '$routeParams', '$timeout', 'AppstoreID', 'XaveeRankingsAPI', 'Rankings', 'Countries', 'RankingTypes', 'Categories', 'Price', 
                           function($scope, $routeParams, $timeout, AppstoreID, XaveeRankingsAPI, Rankings, Countries, RankingTypes, Categories, Price) {
	
	$scope.platformButton = $routeParams.platform || CONSTS.defaults.platform;
	$scope.activeCountry = $routeParams.country || CONSTS.langToCountry[$scope.activeLanguage];
	$scope.activeRankingType = $routeParams.rankingType || CONSTS.defaults.rankingType;
	$scope.activeCategoryID = $routeParams.category || CONSTS.defaults.category;
	
	Rankings.setActiveRanking("xavee");
	Countries.setActiveCountry($scope.activeCountry);
	RankingTypes.setActiveRankingType($scope.activeRankingType);
	RankingTypes.setActiveRankingTypeList("xavee");
	Categories.setActiveCategory($scope.activeCategoryID);
	
	$scope.pageSize = 25;
	$scope.currentPage = 1;
	$scope.ranking = {};
	$scope.ranking.ranking = [];
	$scope.updating = false;
	
	var updateRanking = function() {
		
		XaveeRankingsAPI.ranking({
			// API URL/query parameters.
			country:$scope.activeCountry,
			platform: $scope.platformButton,
			ranking_type:$scope.activeRankingType,
			category:$scope.activeCategoryID,
			page: $scope.currentPage
			
		}, function(data) {
					
			var ranking = data.results;
			
			// Code for the fade-in cascade visual effect.
			var time = 0;
			_.each(ranking, function(entry) {
				$timeout(function () { $scope.ranking.ranking.push(entry); }, time); 
				time += 30;
			});
			
			$scope.updating = false;
		});
	};

	updateRanking();
    
	$scope.getPrice = function(currency, price) {
		return Price.getPrice(currency, price);
	}
	
    $scope.numberOfPages = function() {
        return Math.ceil($scope.ranking.results[0].ranking.length/$scope.pageSize);
    };

    $scope.loadMore = function() {
    	if(!$scope.updating) {
    		$scope.updating = true;
    		$scope.pageSize = $scope.pageSize + 25;
	    	$scope.currentPage++;
	    	updateRanking();
    	}
	    	
    };
	
	$scope.setAppstoreID = function(id, country) {
		AppstoreID.setAppstoreID(id, country);
	}
}]);
	