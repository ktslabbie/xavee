/** 
 * Created on May 18, 2014
 * 
 * @author Kristian
 * 
 * File for Angular API services.
 */

var apiService = angular.module('service.api', ['ngResource'])

.factory('PostsAPI', ['$resource', function($resource) {
    return $resource('/api/posts/:slug', { slug: '@slug' });
}])

.factory('AppsAPI', ['$resource', function($resource) {
    return $resource('/api/apps/:id', { id: '@id' }, {
    				list: { isArray:true,  method:'get', transformResponse: function (data, headers) { return JSON.parse(data).results; }},
    				app:  { isArray:false, method:'get' }
    });
}])

.factory('DevelopersAPI', ['$resource', function($resource) {
    return $resource('/api/apps/developers/:id/', { id: '@id' }, {
    				ranking: { isArray: false, method: 'get' },
    				developer:  { isArray:false, method:'get' }
    });
}])

.factory('RankingsAPI', ['$resource', function($resource) {
    return $resource('/api/apps/world-rankings/:country/:platform/:ranking_type/:category', {
    				country: '@country', platform: '@platform', ranking_type: '@ranking_type', category: '@category' }, {
    				ranking: { isArray: false, method: 'get' }
    });
}])

.factory('XaveeRankingsAPI', ['$resource', function($resource) {
    return $resource('/api/apps/xavee-rankings/:country/:platform/:ranking_type/:category', {
    				country: '@country', platform: '@platform', ranking_type: '@ranking_type', category: '@category' }, {
    				ranking: { isArray: false, method: 'get' }
    });
}])

.factory('ITunesAppLookup', ['$resource', function($resource) {
    return $resource('https://itunes.apple.com/lookup', { id: '@id', country: '@country', }, {
    				itunesApp: { isArray:false, method:'JSONP', params : {callback : 'JSON_CALLBACK'},
    					         transformResponse: function (data, headers) { return angular.fromJson(data).results[0]; } }
    });
}])
