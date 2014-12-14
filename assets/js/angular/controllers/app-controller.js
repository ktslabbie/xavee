/** 
 * Created on May 18, 2014
 * 
 * @author Kristian
 * 
 * File for Angular.js controllers.
 */
var xaveeController = angular.module('xavee.app-controller', [])

// Controller for the App detail page.
.controller('AppController', ['$rootScope', '$scope', '$controller', '$q', '$translate', '$route', '$http', 'app', 'StoreID', 'ITunesApp', 
                              function($rootScope, $scope, $controller, $q, $translate, $route, $http, app, StoreID, ITunesApp) {

	angular.extend(this, $controller('BaseController', {$scope: $scope}));

	$scope.app = app;
	$scope.itunesApp;
	
	$scope.numberOfOverallRankings = 0;
	$scope.numberOfCategoryRankings = 0;
	$scope.rankings = [];
	$scope.showTopRankings = true;
	$scope.showTopCatRankings = true;
	$scope.showVersions = true;
	$scope.xaveeRatingClass = "text-muted";
	$scope.averageRatingClass = "text-muted";
	$scope.descriptionPanelClass = "description-panel-closed";

	var getRatings = function(rating, count) {
		if(rating < 2.75) $scope.averageRatingClass = "text-danger";
		else if(rating < 4) $scope.averageRatingClass = "text-warning";
		else $scope.averageRatingClass = "text-success";
		
		if($scope.app.xavee_score < 50) $scope.xaveeRatingClass = "text-danger";
		else if($scope.app.xavee_score < 80) $scope.xaveeRatingClass = "text-warning";
		else $scope.xaveeRatingClass = "text-success";
	}
	
	if(StoreID.getAppstoreID() != 0) {
		$scope.itunesApp = ITunesApp.itunesApp({id: StoreID.getAppstoreID(), country: StoreID.getAppstoreCountry() });
	}
	
	$q.when($scope.app.$promise).then(function() {
		getRatings($scope.app.itunes_world_rating, $scope.app.itunes_world_rating_count);
		
		var countries = _.map($scope.app.iphone_versions, 'country');
		var versionsOrdered = [];
		
		_.each(COUNTRY_ORDERING[$rootScope.activeLanguage], function(country) {
			if (countries.indexOf(country) > -1) {
				versionsOrdered.push(_.find($scope.app.iphone_versions, { 'country' : country }));
		    }
		});
		
		$scope.app.iphone_versions = versionsOrdered;
		$scope.itunesApp = $scope.itunesApp || ITunesApp.itunesApp({id: $scope.app.iphone_versions[0].appstore_id, country: $scope.app.iphone_versions[0].country });
		
		$translate(['FREE', 'PAID', 'GROSSING',]).then(function (translations) {
			_.each($scope.app.iphone_versions, function(version) {
				_.each(version.rankings, function(ranking) {
					$scope.hasAchievements = true;
					ranking['country'] = version.country;
					ranking['ranking_type_str'] = RANKING_TYPE_TO_STR[ranking.ranking_type].toLowerCase();
					ranking['ranking_type_loc_str'] = translations[RANKING_TYPE_TO_STR[ranking.ranking_type]];
					if(ranking.category.id == 0 || ranking.category.id == 6014)
						$scope.numberOfOverallRankings++;
					else
						$scope.numberOfCategoryRankings++;
					$scope.rankings.push(ranking);
				});
			});
		});
		
		$q.when($scope.itunesApp.$promise).then(function() { $scope.$broadcast('dataloaded'); });
	});
}]);