/** 
 * Created on May 18, 2014
 * 
 * @author Kristian
 * 
 * File for Angular.js controllers.
 */
var appCtrl = angular.module('ctrl.app', [])

// Controller for the App detail page.
.controller('AppCtrl', ['$scope', '$q', 'app', 'Price', 'Countries', 'AppstoreID', 'ITunesAppLookup', 
                              function($scope, $q, app, Price, Countries, AppstoreID, ITunesAppLookup) {

	$scope.app = app;
	$scope.itunesApp;
	
	$scope.numberOfOverallRankings = 0;
	$scope.numberOfCategoryRankings = 0;
	$scope.rankings = [];
	$scope.showTopRankings = true;
	$scope.showTopCatRankings = true;
	$scope.showVersions = true;
	$scope.descriptionPanelClass = "description-panel-closed";
	
	if(AppstoreID.getAppstoreID() != 0) {
		$scope.itunesApp = ITunesAppLookup.itunesApp({id: 	AppstoreID.getAppstoreID(), 
												 country: 	AppstoreID.getAppstoreCountry() });
	}
	
	$q.when($scope.app.$promise).then(function() {
		$scope.itunesApp = $scope.itunesApp || ITunesAppLookup.itunesApp({id: 	$scope.app.iphone_versions[0].appstore_id, 
																	 country: 	Countries.getActiveCountry() });
		
		_.each($scope.app.iphone_versions, function(version) {
			_.each(version.rankings, function(ranking) {
				$scope.hasAchievements = true;
				ranking['country'] = version.country;
				ranking['ranking_type_str'] = CONSTS.rankingTypeLists.world[ranking.ranking_type - 1];
				
				if(ranking.category.id == 0 || ranking.category.id == 6014)
					$scope.numberOfOverallRankings++;
				else
					$scope.numberOfCategoryRankings++;
				$scope.rankings.push(ranking);
			});
		});
		
		$q.when($scope.itunesApp.$promise).then(function() { $scope.$broadcast('dataloaded'); });
	});
	
	$scope.getPrice = Price.getPrice;
}]);