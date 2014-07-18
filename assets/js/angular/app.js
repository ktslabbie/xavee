/** 
 * Created on May 18, 2014
 * 
 * @author Kristian
 * 
 * File for Angular.js apps.
 */

xaveeApp = angular.module('xavee.app', ['xavee.api', 'xavee.controller']);

xaveeApp.config(function($interpolateProvider) {
	$interpolateProvider.startSymbol('{[{');
	$interpolateProvider.endSymbol('}]}');
});
