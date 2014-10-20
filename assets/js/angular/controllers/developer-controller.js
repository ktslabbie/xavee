/** 
 * Created on May 18, 2014
 * 
 * @author Kristian
 * 
 * File for Angular.js controllers.
 */
var xaveeController = angular.module('xavee.developer-controller', [])

// Controller for the Ranking page.
.controller('DeveloperController', ['$scope', '$routeParams', '$location', 'developer', 
                                       function($scope, $routeParams, $location, developer) {
	
	//$scope.developer = Developer.developer({id:$routeParams.developerID});
	$scope.developer = developer;
}]);
	