/** 
 * Created on May 18, 2014
 * 
 * @author Kristian
 * 
 * File for Angular.js directives.
 */

xaveeApp.directive('back', ['$window', function($window) {
    return {
        restrict: 'A',
        link: function (scope, elem, attrs) {
            elem.bind('click', function () {
                $window.history.back();
            });
        }
    };
}]);