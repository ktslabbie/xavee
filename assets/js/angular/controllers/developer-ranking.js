/** 
 * Created on May 18, 2014
 * 
 * @author Kristian
 * 
 * File for Angular.js controllers.
 */
var xrCtrl = angular.module('ctrl.developer-ranking', [])

// Controller for the Ranking page.
.controller('DeveloperRankingCtrl', ['$scope', '$routeParams', '$timeout', 'AppstoreID', 'DevelopersAPI', 'Rankings', 'RankingTypes', 'Categories', 
                           function($scope, $routeParams, $timeout, AppstoreID, DevelopersAPI, Rankings, RankingTypes, Categories) {
	
	$scope.platformButton = $routeParams.platform || CONSTS.defaults.platform;
	$scope.activeRankingType = 'developers';
	$scope.activeCategoryID = $routeParams.category || CONSTS.defaults.category;
	
	Rankings.setActiveRanking('xavee');
	RankingTypes.setActiveRankingType('developers');
	RankingTypes.setActiveRankingTypeList('xavee');
	Categories.setActiveCategory($scope.activeCategoryID);
	
	$scope.pageSize = 25;
	$scope.currentPage = 1;
	$scope.ranking = {};
	$scope.ranking.ranking = [];
	$scope.updating = false;
	
	var updateRanking = function() {
		
		DevelopersAPI.ranking({
			// API URL/query parameters.
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
}]);
	