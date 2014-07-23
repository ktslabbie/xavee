/** 
 * Created on May 18, 2014
 * 
 * @author Kristian
 * 
 * File for Angular.js controllers.
 */

var xaveeAPIService = angular.module('xavee.api', ['ngResource']);

xaveeAPIService.factory('Post', ['$resource', function($resource) {
    return $resource('/api/posts/:slug', { slug: '@slug' });
}]);
