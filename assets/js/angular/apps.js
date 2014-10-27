/** 
 * Created on May 18, 2014
 * 
 * @author Kristian
 * 
 * File for Angular.js apps.
 */

xaveeApp = angular.module('xavee.app', ['ngRoute', 'xavee.api', 'xavee.worldranking-controller', 
                                        'xavee.app-controller', 'xavee.developer-controller', 'xavee.tl-controller',
                                        'infinite-scroll', 'pascalprecht.translate'])

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

// White-list Amazon S3, since our templates need to be loaded from there.
.config(['$sceDelegateProvider', function($sceDelegateProvider) {
	$sceDelegateProvider.resourceUrlWhitelist([
        'self',
        'https://xavee.s3.amazonaws.com/**',
    ]);
}])

// Configure routes.
.config(function($routeProvider, $locationProvider) {
	// Set base URL.
	$('html').append( '<base href="/' + window.location.pathname.split("/")[1] + '/apps/">');
	
	$routeProvider
		// Route for the rankings page.
		.when('/world-rankings/:country/:platform/:ranking_type/:category', {
			templateUrl : TEMPLATE_BASE + '/worldranking.html',
			controller: 'RankingController'
		})
		
		// Route for the developer detail pages.
		.when('/developers/:developerID*', {
			templateUrl : TEMPLATE_BASE + '/developer-detail.html',
			controller: 'DeveloperController',
			resolve: {
	            developer: function($route, Developer) {
	            	var devID = $route.current.params.developerID.split('/')[0];
	                return Developer.developer({id:devID});
	            }
	        }
		})
		
		// Route for the app detail pages.
		.when('/:appID*', {
			templateUrl : TEMPLATE_BASE + '/app-detail.html',
			controller: 'AppController',
			resolve: {
	            app: function($route, App) {
	            	var appID = $route.current.params.appID.split('/')[0];
	                return App.app({id:appID});
	            }
	        }
		})
		
		.otherwise({
		    redirectTo: '/world-rankings/us/iphone/free/6014'
		});
	
	$locationProvider.html5Mode(true);
    $locationProvider.hashPrefix('!');
})

.run(function($rootScope, $http, $location, $translate) {
	// Bind the image base dir to the root scope.
	$rootScope.IMG_BASE = IMG_BASE;
	$rootScope.TEMPLATE_BASE = TEMPLATE_BASE;
	
	// Bind translation handlers to the root scope.
	$rootScope.activeLanguage = $location.absUrl().split('/')[3];
	$http.defaults.headers.common['Accept-Language'] = $rootScope.activeLanguage;
	$translate.use($rootScope.activeLanguage);
	
	$rootScope.changeActiveLanguage = function(lang) {
		$rootScope.activeLanguage = lang;
		$translate.use($rootScope.activeLanguage);
	};
	
	// Bind the `$locationChangeSuccess` event on the rootScope, so that we dont need to 
	// bind in individual controllers.
//	$rootScope.$on('$locationChangeSuccess', function() {
//		$rootScope.actualSearch = $location.search();
//	});
});
