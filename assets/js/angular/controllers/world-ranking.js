/** 
 * Created on May 18, 2014
 * 
 * @author Kristian
 * 
 * File for Angular.js controllers.
 */
var wrCtrl = angular.module('ctrl.world-ranking', [])

// Controller for the Ranking page.
.controller('WorldRankingCtrl', ['$scope', '$routeParams', '$timeout', 'AppstoreID', 'RankingsAPI', 'Rankings', 'Countries', 'RankingTypes', 'Categories', 'Price', 
                                       function($scope, $routeParams, $timeout, AppstoreID, RankingsAPI, Rankings, Countries, RankingTypes, Categories, Price) {
	
	$scope.platformButton = $routeParams.platform || CONSTS.defaults.platform;
	$scope.activeCountry = $routeParams.country || CONSTS.langToCountry[$scope.activeLanguage];
	$scope.activeRankingType = $routeParams.rankingType || CONSTS.defaults.rankingType;
	$scope.activeCategoryID = $routeParams.category || CONSTS.defaults.category;
	
	Rankings.setActiveRanking("world");
	Countries.setActiveCountry($scope.activeCountry);
	RankingTypes.setActiveRankingType($scope.activeRankingType);
	RankingTypes.setActiveRankingTypeList('world');
	Categories.setActiveCategory($scope.activeCategoryID);
	
	$scope.pageSize = 15;
	
	var updateRanking = function() {
		RankingsAPI.ranking({
			
			country:$scope.activeCountry,
			platform: $scope.platformButton, 
			ranking_type:$scope.activeRankingType,
			category:$scope.activeCategoryID
			
		}, function(data) {
												   
			var ranking = data.ranking;
			data.ranking = [];
			$scope.ranking = data;
			
			// Code for the fade-in cascade visual effect.
			var time = 0;
			_.each(ranking, function(entry) {
				$timeout(function () { $scope.ranking.ranking.push(entry); }, time); 
				time += 30;
			});
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
    	$scope.pageSize = $scope.pageSize + 15;
    };
	
	$scope.setAppstoreID = function(id, country) {
		AppstoreID.setAppstoreID(id, country);
	}
}]);
	