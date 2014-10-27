/** 
 * Created on May 18, 2014
 * 
 * @author Kristian
 * 
 * File for Angular.js controllers.
 */
var xaveeController = angular.module('xavee.developer-controller', [])

// Controller for the Ranking page.
.controller('DeveloperController', ['$scope', 'developer', 
                                       function($scope, developer) {
	$scope.developer = developer;
}]);