/** 
 * Created on May 18, 2014
 * 
 * @author Kristian
 * 
 * File for Angular.js controllers.
 */

var xaveeController = angular.module('xavee.controller', []);

xaveeController.controller('PostController', ['$scope', 'Post', function($scope, Post) {
	$scope.posts = Post.query();
}]);

xaveeController.controller('ApplicationController', ['$scope', 'Application', function($scope, Application) {
	$scope.apps = Application.apps();
}]);

xaveeController.controller('ApplicationDetailController', ['$scope', 'Application', function($scope, Application, AppID) {
	
	$scope.app = Application.apps({id:AppID.getID()});
	
}]);

// Controller for the Ranking page.
xaveeController.controller('RankingController', ['$scope', 'Ranking', function($scope, Ranking, AppID) {
	
	countries = [                                                                                                                                                                                                 
		['us', 'United States'],                                                                                                                                                                                                                         
		['jp', 'Japan'],                                                                                                                                                                                                                         
		['gb', 'United Kingdom'],
		['de', 'Germany'],
		['fr', 'France'],
		['kr', 'South Korea'],
		['au', 'Australia'],
		['cn', 'China'],
		['ca', 'Canada'],
		['es', 'Spain'],
		['it', 'Italy'],
		['ru', 'Russia'],
		['nl', 'The Netherlands'],
	];
	
	$scope.platformButton = 'iphone';
	$scope.rankingTypeButton = '1';
	$scope.countryButton = 'us';
	$scope.categoryButton = -1;
	$scope.countries = countries;
	$scope.selected = 0;
	
	$scope.ranking = Ranking.ranking({country:$scope.countryButton, ranking_type:$scope.rankingTypeButton, category:$scope.categoryButton});
	
	$scope.sendID = function(id) {
		AppID.setID(id);
	}
	
	$scope.changeRankingType = function(rankingType) {
		$scope.rankingTypeButton = rankingType;
		$scope.ranking = Ranking.ranking({country:$scope.countryButton, ranking_type:$scope.rankingTypeButton, category:$scope.categoryButton});
		
	};
	
	$scope.changeCountry = function(country, index) {
		$scope.countryButton = country;
		$scope.selected = index;
		$scope.ranking = Ranking.ranking({country:$scope.countryButton, ranking_type:$scope.rankingTypeButton, category:$scope.categoryButton});
		
	};
}]);

// Controller for the rankings per version.
xaveeController.controller('VersionRankingController', ['$scope', 'VersionRanking', function($scope, VersionRanking) {
	$scope.versionRank = VersionRanking.versionRanking({application_id:$scope.rank.version.application.id, ranking_type:$scope.rankingTypeButton});
	
//	$scope.getVersions = function() {
//		return versionRank;
//	};
}]);
	