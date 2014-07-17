/** 
 * Created on May 18, 2014
 * 
 * @author Kristian
 * 
 * File for Angular.js controllers.
 */

var xaveeController = angular.module('xavee.controller', []);

xaveeController.controller('PostController', ['$scope', 'Post', function($scope, Post) {
	$scope.posts = Post.query();
}]);
