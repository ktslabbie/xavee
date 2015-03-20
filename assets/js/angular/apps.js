/** 
 * Created on May 18, 2014
 * 
 * @author Kristian
 * 
 * File for the main Angular Xavee app.
 */

var xavee = angular.module('app.xavee', [
		
		// First party dependencies
		'ngRoute', 'ngAnimate',

		 // Services
		 'service.api', 'service.appstore-id', 'service.category', 'service.country',
		 'service.ranking', 'service.price', 'service.ranking-type',  
		 
		 // Controllers
		 'ctrl.app', 'ctrl.developer', 'ctrl.developer-ranking', 'ctrl.facetbar',
         'ctrl.navbar', 'ctrl.world-ranking', 'ctrl.xavee-ranking',
         
         // Third party dependencies
         'infinite-scroll', 'pascalprecht.translate'
         
])

// Change template variable symbols to avoid overlap with Django's symbols ( {{ }} ).
.config(function($interpolateProvider) {
	$interpolateProvider.startSymbol('{[{');
	$interpolateProvider.endSymbol('}]}');
})

// Set up the languages.
.config(['$translateProvider', function ($translateProvider) {
	// Add translation tables.
	$translateProvider.translations('en', translationsEN);
	$translateProvider.translations('ja', translationsJA);
	$translateProvider.preferredLanguage('en');
	$translateProvider.fallbackLanguage('en');
}])

// Set the HTTP headers to work with CORS.
.config(function($httpProvider) {
	$httpProvider.defaults.useXDomain = true;
	delete $httpProvider.defaults.headers.common['X-Requested-With'];
})

// White-list Amazon S3 and iTunes, since our templates/app info need to be loaded from there.
.config(['$sceDelegateProvider', function($sceDelegateProvider) {
	$sceDelegateProvider.resourceUrlWhitelist([
        'self',
        'https://xavee.s3.amazonaws.com/**',
        'https://itunes.apple.com/**',
    ]);
}])

// Configure routes.
.config(function($routeProvider, $locationProvider) {
	
	// Set base URL that takes into account the current selected language.
	$('html').append( '<base href="/' + window.location.pathname.split("/")[1] + '/">');
	
	$routeProvider
		// Route for the world rankings page.
		.when('/:xavee-rankings/:country/:platform/developers/:category', {
			templateUrl : TEMPLATE_BASE + '/developer-ranking.html',
			controller: 'DeveloperRankingCtrl'
		})
		
		// Route for the xavee rankings page.
		.when('/xavee-rankings/:country/:platform/:rankingType/:category', {
			templateUrl : TEMPLATE_BASE + '/xavee-ranking.html',
			controller: 'XaveeRankingCtrl'
		})
	
		.when('/world-rankings/:country/:platform/:rankingType/:category', {
			templateUrl : TEMPLATE_BASE + '/world-ranking.html',
			controller: 'WorldRankingCtrl'
		})
		
		// Route for the developer detail pages.
		.when('/developers/:developerID*', {
			templateUrl : TEMPLATE_BASE + '/developer-detail.html',
			controller: 'DeveloperCtrl',
			resolve: {
	            developer: function($route, DevelopersAPI) {
	            	var devID = $route.current.params.developerID.split('/')[0];
	                return DevelopersAPI.developer({id:devID});
	            }
	        }
		})
		
		// Route for the app detail pages.
		.when('/apps/:appID*', {
			templateUrl : TEMPLATE_BASE + '/app-detail.html',
			controller: 'AppCtrl',
			resolve: {
	            app: function($route, AppsAPI) {
	            	var appID = $route.current.params.appID.split('/')[0];
	                return AppsAPI.app({id:appID});
	            }
	        }
		})
		
		.otherwise({
		    redirectTo: '/world-rankings/us/iphone/free/6014'
		});
	
	$locationProvider.html5Mode(true);
    $locationProvider.hashPrefix('!');
})

// Initialize variables.
.run(function($rootScope, $http, $location, $translate) {
	
	// Bind the image base dir to the root scope.
	$rootScope.IMG_BASE = IMG_BASE;
	$rootScope.TEMPLATE_BASE = TEMPLATE_BASE;
	
	// Bind translation handlers to the root scope.
	$rootScope.activeLanguage = $location.absUrl().split('/')[3];
	$http.defaults.headers.common['Accept-Language'] = $rootScope.activeLanguage;
	$translate.use($rootScope.activeLanguage);
	
	// Bind a function for changing the language to the root scope.
	$rootScope.changeActiveLanguage = function(lang) {
		$rootScope.activeLanguage = lang;
		$translate.use($rootScope.activeLanguage);
	};
	
	// Bind a function for converting dash-separated strings to camelCase.
	$rootScope.camelCase = function(string) {
		console.log("hi camelCase: " + string);
		return string.toLowerCase().replace(/-(.)/g, function(match, group1) {
	        return group1.toUpperCase();
	    });
	};
});
