/** 
 * Created on May 18, 2014
 * 
 * @author Kristian
 * 
 * File for Angular.js services.
 */

var xaveeService = angular.module('xavee.api', ['ngResource']);

xaveeService.factory('StoreID', function() {
    var itunesID = 0, country = 'us';
    
    return {
    	setAppstoreID: function(id, cntry) {
    		itunesID = id;
    		country = cntry;
    	},
    	
        getAppstoreID: function() {
            return itunesID;
        },
    	
    	getAppstoreCountry: function() {
            return country;
        }
    }
});

xaveeService.factory('Post', ['$resource', function($resource) {
    return $resource('/api/posts/:slug', { slug: '@slug' });
}]);

xaveeService.factory('App', ['$resource', function($resource) {
    return $resource('/api/apps/:id', { id: '@id' }, {
    					list: { isArray:true,  method:'get', transformResponse: function (data, headers) { return JSON.parse(data).results; }},
    					app:  { isArray:false, method:'get' }
    });
}]);

xaveeService.factory('Developer', ['$resource', function($resource) {
    return $resource('/api/apps/developers/:id', { id: '@id' }, {
    					list: 		{ isArray:true,  method:'get', transformResponse: function (data, headers) { return JSON.parse(data).results; }},
    					developer:  { isArray:false, method:'get' }
    });
}]);

xaveeService.factory('WorldRanking', ['$resource', function($resource) {
    return $resource('/api/apps/world-rankings/:country/:platform/:ranking_type/:category',
    				{	country: '@country', platform: '@platform', ranking_type: '@ranking_type', category: '@category' }, {
    					ranking: { isArray:false, method:'get' }
    				});
}]);

xaveeService.factory('ITunesApp', ['$resource', function($resource) {
    return $resource('https://itunes.apple.com/lookup',
    				{	id: '@id', country: '@country', }, {
    					itunesApp: { isArray:false, method:'JSONP', params : {callback : 'JSON_CALLBACK'}, transformResponse: function (data, headers) {
    									 return angular.fromJson(data).results[0]; } }
    				});
}]);
