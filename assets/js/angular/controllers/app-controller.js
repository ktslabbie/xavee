/** 
 * Created on May 18, 2014
 * 
 * @author Kristian
 * 
 * File for Angular.js controllers.
 */
var xaveeController = angular.module('xavee.app-controller', [])

// Controller for the Ranking page.
.controller('AppController', ['$scope', 'app', 
                                       function($scope, app) {

	$scope.app = app;
}]);