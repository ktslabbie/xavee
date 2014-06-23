/** 
 * Created on May 18, 2014
 * 
 * @author Kristian
 * 
 * Main Javascript file. 
 * All Javascript that is run on every page must go in here.
 */

/*
 * Angular.js code.
 */
app = angular.module('xavee.app.basic', []);

app.config(function($interpolateProvider) {
	$interpolateProvider.startSymbol('{[{');
	$interpolateProvider.endSymbol('}]}');
});

app.controller('AppController', ['$scope', '$http', function($scope, $http) {
	$scope.posts = [];
    $http.get('/api/posts').then(function(result) {
        angular.forEach(result.data.results, function(item) {
            $scope.posts.push(item);
        });
    });
}]);


/*
 * Misc. jQuery code.
 */
//$(document).ready(function() {
//	if ($('#referralRedirect').length) {		
//		ga('send', 'pageview', {
//			  'dimension1': referralName,
//			  'dimension2': referralPlatform,
//			  'dimension3': referralSource,
//			  'dimension4': referralMedium,
//			});
//		ga(function() {
//			window.location.replace(referralDestination);
//		});
//    }
//});
