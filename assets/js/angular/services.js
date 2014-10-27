/** 
 * Created on May 18, 2014
 * 
 * @author Kristian
 * 
 * File for Angular.js services.
 */

var xaveeAPIService = angular.module('xavee.api', ['ngResource']);

xaveeAPIService.factory('Post', ['$resource', function($resource) {
    return $resource('/api/posts/:slug', { slug: '@slug' });
}]);

xaveeAPIService.factory('App', ['$resource', function($resource) {
    return $resource('/api/apps/:id', { id: '@id' }, {
    					list: { isArray:true,  method:'get', transformResponse: function (data, headers) { return JSON.parse(data).results; }},
    					app:  { isArray:false, method:'get' }
    });
}]);

xaveeAPIService.factory('Developer', ['$resource', function($resource) {
    return $resource('/api/apps/developers/:id', { id: '@id' }, {
    					list: 		{ isArray:true,  method:'get', transformResponse: function (data, headers) { return JSON.parse(data).results; }},
    					developer:  { isArray:false, method:'get' }
    });
}]);

xaveeAPIService.factory('WorldRanking', ['$resource', function($resource) {
    return $resource('/api/apps/world-rankings/:country/:platform/:ranking_type/:category',
    				{	country: '@country', platform: '@platform', ranking_type: '@ranking_type', category: '@category' }, {
    					ranking: { isArray:false, method:'get' }
    				});
}]);
