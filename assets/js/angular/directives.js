/** 
 * Created on May 18, 2014
 * 
 * @author Kristian
 * 
 * File for Angular.js directives.
 */

// Directive for a back button using the HTML5 History API.
xaveeApp.directive('back', ['$window', function($window) {
    return {
        restrict: 'A',
        link: function (scope, elem, attrs) {
            elem.bind('click', function () {
                $window.history.back();
            });
        }
    };
}])

.directive('seeMore', ['$timeout', function ($timeout) {
    return {
        link: function (scope, element, attrs) {
            scope.$on('dataloaded', function () {
                $timeout(function () { // You might need this timeout to be sure its run after DOM render.
                	if(element.height() < element.prop('scrollHeight')) {
                		element.next().html(
                			'<a class="pointer" onClick="$(\'#description\').toggleClass(\'description-panel-open description-panel-closed\'); $(\'#seemore\').remove()">See more...</a>');
                	}
                }, 0, false);
            })
        }
    };
}]);
