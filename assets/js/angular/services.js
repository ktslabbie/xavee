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

xaveeAPIService.factory('Application', ['$resource', function($resource) {
    return $resource('/api/apps/:id', { id: '@id' }, {
    					//list: { isArray:true, method:'get', transformResponse: function (data, headers) { return JSON.parse(data).results; }},
    					apps: { isArray:false, method:'get' }
    				});
}]);

xaveeAPIService.factory('Ranking', ['$resource', function($resource) {
    return $resource('/api/apps/rankings?country=:country', { country: '@country' }, {
    					//list: { isArray:true, method:'get', transformResponse: function (data, headers) { return JSON.parse(data).results; }},
    					ranking: { isArray:false, method:'get' }
    				});
}]);

xaveeAPIService.factory('VersionRanking', ['$resource', function($resource) {
    return $resource('/api/apps/:application_id/versions?ranking_type=:ranking_type', { application_id: '@application_id', ranking_type: '@ranking_type' }, {
    					versionRanking: { isArray:false, method:'get' }
    				});
}]);

xaveeAPIService.factory('AppID', function() {
	  var appID = -1;

	  var setID = function(id) {
	      appID = id;
	  }

	  var getID = function(){
	      return appID;
	  }
});
