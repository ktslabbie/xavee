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
.controller('RankingController', ['$scope', '$rootScope', '$location', '$controller', 'Ranking', 
                                       function($scope, $rootScope, $location, $controller, Ranking) {
	angular.extend(this, $controller('BaseController', {$scope: $scope}));
	angular.extend(this, $controller('TLController', {$scope: $scope}));
	
	var updateEnvironment = function() {
		$scope.platformButton = $location.search().platform || "iphone";
		$scope.rankingTypeButton = $location.search().ranking || 1;
		$scope.countryButton = $location.search().country || LANG_TO_COUNTRY[$scope.activeLanguage];
		$scope.activeCategoryID = $location.search().category || 6014;
		$scope.activeGameCategory = 6014;
		$scope.activeAppCategory = 0;
		$scope.selectedCountry = COUNTRY_TO_INDEX[$scope.countryButton];
		$scope.appType = ($scope.activeCategoryID == 6014 || $scope.activeCategoryID > 6999) ? 1 : 2;
		
		if($scope.appType == 1) {
			$scope.activeGameCategory = $scope.activeCategoryID;
		} else {
			$scope.activeAppCategory = $scope.activeCategoryID;
		}
	}
	
	var updateRanking = function() {
		$scope.pageSize = 20;
		$scope.ranking = Ranking.ranking({country:$scope.countryButton, ranking_type:$scope.rankingTypeButton, category:$scope.activeCategoryID});
	};
	
	var updatePage = function() {
		$location.search({platform: $scope.platformButton, country: $scope.countryButton, category: $scope.activeCategoryID, ranking: $scope.rankingTypeButton});
		updateRanking();
	};
	
	var LANG_TO_COUNTRY = { 'en': 'us', 'ja': 'jp' };
	var COUNTRY_TO_INDEX = { 'us': 0, 'jp': 1, 'gb': 2, 'de': 3, 'fr': 4, 'kr': 5, 'au': 6, 'cn': 7, 'ca': 8, 'es': 9, 'it': 10, 'ru': 11, 'nl': 12 };

	
	updateEnvironment();
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
	
	$rootScope.$watch(function () { return $location.search() }, function (newSearch, oldSearch) {
		
		// Check for back/forward button press.
		if($rootScope.actualSearch === newSearch) {
			updateEnvironment();
			updateRanking();
	    }
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
	