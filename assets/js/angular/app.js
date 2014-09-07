/** 
 * Created on May 18, 2014
 * 
 * @author Kristian
 * 
 * File for Angular.js apps.
 */

xaveeApp = angular.module('xavee.app', ['xavee.api', 'xavee.controller', 'infinite-scroll']);

xaveeApp.config(function($interpolateProvider) {
	$interpolateProvider.startSymbol('{[{');
	$interpolateProvider.endSymbol('}]}');
});

//We already have a limitTo filter built-in to angular,
//let's make a startFrom filter
xaveeApp.filter('startFrom', function() {
	return function(input, start) {
		start = +start; //parse to int
		if (input) return input.slice(start);
	}
});