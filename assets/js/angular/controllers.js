/** 
 * Created on May 18, 2014
 * 
 * @author Kristian
 * 
 * File for Angular.js controllers.
 */
var xaveeController = angular.module('xavee.controller', [])

.controller('BaseController', ['$scope', '$http', '$location', '$translate', function($scope, $http, $location, $translate) {
	$scope.activeLanguage = $location.absUrl().split('/')[3];
	$http.defaults.headers.common['Accept-Language'] = $scope.activeLanguage;
	$translate.use($scope.activeLanguage);
	
	$scope.changeActiveLanguage = function(lang) {
		$scope.activeLanguage = lang;
		$translate.use($scope.activeLanguage);
	};
}])

// Controller for the Ranking page.
.controller('RankingController', ['$scope', '$rootScope', '$location', '$controller', '$routeParams', 'Ranking', 
                                       function($scope, $rootScope, $location, $controller, $routeParams, Ranking) {
	angular.extend(this, $controller('BaseController', {$scope: $scope}));
	
	var updateRanking = function() {
		$scope.pageSize = 20;
		$scope.ranking = Ranking.ranking({country:$scope.countryButton, ranking_type:$scope.rankingTypeButton, category:$scope.activeCategoryID});
	};
	
	$scope.platformButton = 'iphone';
	$scope.rankingTypeButton = '1';
	$scope.countryButton = 'us';
	$scope.activeCategoryID = 6014;
	
	$scope.selected = 0;
	$scope.appType = 1;
	$location.search({platform: $scope.platformButton, country: $scope.countryButton, category: $scope.activeCategoryID, ranking: $scope.rankingTypeButton});
	
	//updateRanking();
    
    $scope.numberOfPages = function() {
        return Math.ceil($scope.ranking.results[0].ranking.length/$scope.pageSize);
    };

    $scope.loadMore = function() {
    	$scope.pageSize = $scope.pageSize + 20;
    };
	
	$scope.changeRankingType = function(rankingType) {
		$scope.rankingTypeButton = rankingType;
		$location.search({platform: $scope.platformButton, country: $scope.countryButton, category: $scope.activeCategoryID, ranking: $scope.rankingTypeButton});
		//updateRanking();
	};
	
	$scope.changeCountry = function(country, index) {
		$scope.countryButton = country;
		$scope.selected = index;
		$location.search({platform: $scope.platformButton, country: $scope.countryButton, category: $scope.activeCategoryID, ranking: $scope.rankingTypeButton});
		//updateRanking();
	};
	
	$scope.changeAppType = function(appType, category) {
		$scope.appType = appType;
		$scope.activeCategoryID = category.id;
		$location.search({platform: $scope.platformButton, country: $scope.countryButton, category: $scope.activeCategoryID, ranking: $scope.rankingTypeButton});
		//updateRanking();
	};
	
	$scope.changeCategory = function(category) {
		$scope.activeCategoryID = category.id;
		$location.search({platform: $scope.platformButton, country: $scope.countryButton, category: $scope.activeCategoryID, ranking: $scope.rankingTypeButton});
		//updateRanking();
	};
	
	$rootScope.$on("$locationChangeSuccess", function (locationChangeObj, path) {
		$scope.countryButton = $location.search().country;
		$scope.activeCategoryID = $location.search().category;
		$scope.rankingTypeButton = $location.search().ranking;
		$scope.platformButton = $location.search().platform;
		updateRanking();
	});

}])

.controller('PostController', ['$scope', '$controller', 'Post', function($scope, $controller, Post) {
	angular.extend(this, $controller('BaseController', {$scope: $scope}));
	$scope.posts = Post.query();
}])

.controller('ApplicationController', ['$scope', '$controller', 'Application', function($scope, $controller, Application) {
	angular.extend(this, $controller('BaseController', {$scope: $scope}));
	$scope.apps = Application.apps();
}])

.controller('ApplicationDetailController', ['$scope', 'Application', function($scope, Application, AppID) {
	$scope.app = Application.apps({id:AppID.getID()});
}]);
	