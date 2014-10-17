/** 
 * Created on May 18, 2014
 * 
 * @author Kristian
 * 
 * File for Angular.js apps.
 */

xaveeApp = angular.module('xavee.app', ['ngRoute', 'xavee.api', 'xavee.controller', 'xavee.tlcontroller',
                                        'infinite-scroll', 'pascalprecht.translate'])
                                        
.config(function($interpolateProvider) {
	$interpolateProvider.startSymbol('{[{');
	$interpolateProvider.endSymbol('}]}');
})

.config(['$translateProvider', function ($translateProvider) {
	// add translation tables
	$translateProvider.translations('en', translationsEN);
	$translateProvider.translations('ja', translationsJA);
	$translateProvider.preferredLanguage('en');
	$translateProvider.fallbackLanguage('en');
}])

.config(function($httpProvider) {
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
})

// Configure routes.
.config(function($routeProvider, $locationProvider) {
	// Set base URL.
	$('html').append( '<base href="/' + window.location.pathname.split("/")[1] + '/apps/">');
	
	$routeProvider
		// route for the apps page
		.when('/', {
			templateUrl : TEMPLATE_BASE + '/application-ranking.html',
			controller: 'RankingController'
		});
	
	$locationProvider.html5Mode(true);
    $locationProvider.hashPrefix('!');
})

.run(function($rootScope, $location) {
	// Bind the image base dir to the root scope.
	$rootScope.IMG_BASE = IMG_BASE;
	$rootScope.TEMPLATE_BASE = TEMPLATE_BASE;
	
	// Bind the `$locationChangeSuccess` event on the rootScope, so that we dont need to 
	// bind in individual controllers.
	$rootScope.$on('$locationChangeSuccess', function() {
		$rootScope.actualSearch = $location.search();
	});
});

//// We already have a limitTo filter built-in to angular, let's make a startFrom filter.
//.filter('startFrom', function() {
//	return function(input, start) {
//		start = +start; //parse to int
//		if (input) return input.slice(start);
//	}
//});