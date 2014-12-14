/** 
 * Created on May 18, 2014
 * 
 * @author Kristian
 * 
 * File for Angular.js controllers.
 */
var xaveeController = angular.module('xavee.nav-controller', [])

// Controller for the navigation bar (mostly search?)
.controller('NavController', ['$scope', '$location', 'App', function($scope, $location, App) {
	
	var requests = 0;
	$scope.resolved = false;
	$scope.searchQuery;
	$scope.searchResults;
	
	$scope.query = function() {
		requests++;
		$scope.resolved = false;
		if($scope.searchQuery) {
			$scope.searchResults = App.list({results: 5, q: $scope.searchQuery }, function() {
				requests--;
				if(requests <= 0) $scope.resolved = true;
			});
		} else {
			requests = 0;
		}
	}
	
	$scope.$on('$locationChangeStart', function(event) {
	    $scope.searchQuery = null;
	    $scope.searchResults = null;
	});
}]);