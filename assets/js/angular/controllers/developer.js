/** 
 * Created on May 18, 2014
 * 
 * @author Kristian
 * 
 * File for Angular.js controllers.
 */
var developerCtrl = angular.module('ctrl.developer', [])

// Controller for the Ranking page.
.controller('DeveloperCtrl', ['$scope', 'developer', 'AppstoreID', 
                                       function($scope, developer, AppstoreID) {
	
	$scope.developer = developer;
	
	$scope.setAppstoreID = function(id) {
		AppstoreID.setAppstoreID(id);
	}
}]);