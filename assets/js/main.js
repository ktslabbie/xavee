/** 
 * Created on May 18, 2014
 * 
 * @author Kristian
 * 
 * Main Javascript file. 
 * All Javascript that is run on every page must go in here.
 */

/*
 * Angular.js code.
 */
app = angular.module('xavee.app.api', ['ngResource']);

app.factory('Post', ['$resource', function($resource) {
    return $resource('/api/posts/:id', { id: '@id' });
}]);

app = angular.module('xavee.app.resource', ['xavee.app.api']);

app.config(function($interpolateProvider) {
	$interpolateProvider.startSymbol('{[{');
	$interpolateProvider.endSymbol('}]}');
});

app.controller('AppController', ['$scope', 'Post', function($scope, Post) {
	$scope.selected = 0;
	$scope.itemClicked = function ($index) {
	    $scope.selected = $index;
	};
	
	$scope.posts = Post.query();
}]);

/*
 * Misc. jQuery code.
 */

$(function () {
	//use local CSS file as fallback if Bootstrap CDN fails
	if ($('#css-check').is(':visible') === true) {
		$('<link rel="stylesheet" type="text/css" href="/static/css/vendor/bootstrap.min.css">').appendTo('head');
	}
});

//$(document).ready(function() {
//	if ($('#referralRedirect').length) {		
//		ga('send', 'pageview', {
//			  'dimension1': referralName,
//			  'dimension2': referralPlatform,
//			  'dimension3': referralSource,
//			  'dimension4': referralMedium,
//			});
//		ga(function() {
//			window.location.replace(referralDestination);
//		});
//    }
//});
