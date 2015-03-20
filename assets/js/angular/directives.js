/** 
 * Created on May 18, 2014
 * 
 * @author Kristian
 * 
 * File for Angular.js directives.
 * 
 * Can be kept in a single file while it remains small;
 * consider splitting once it gets too large.
 */

/**
 *  Directive for a back button using the HTML5 History API (unused).
 */
xavee.directive('back', ['$window', function($window) {
    return {
        restrict: 'A',
        link: function (scope, elem, attrs) {
            elem.bind('click', function () {
                $window.history.back();
            });
        }
    };
}])

/**
 * Directive to expand an app's description.
 */
.directive('seeMore', ['$timeout', function ($timeout) {
    return {
        link: function (scope, element, attrs) {
            scope.$on('dataloaded', function () {
                $timeout(function () { // You need this timeout to be sure its run after DOM render.
                	if(element.height() < element.prop('scrollHeight')) {
                		element.next().html(
                			'<a class="pointer" onClick="$(\'#description\')' +
                				'.toggleClass(\'description-panel-open description-panel-closed\'); $(\'#seemore\').remove()">See more...</a>');
                	}
                });
            })
        }
    };
}])

/**
 * Directive to give the iTunes rating a color.
 */
.directive('itunesRating', function () {
    return {
        link: function (scope, element, attrs) {
        	scope.$watch('app.itunes_world_rating', function(itunes_world_rating) {
	        	if(itunes_world_rating < 2.75) element.addClass("text-danger");
	    		else if(itunes_world_rating < 4) element.addClass("text-warning");
	    		else element.addClass("text-success");
        	});
        }
    };
})

/**
 * Directive to give the Xavee score a color.
 */
.directive('xaveeScore', function () {
    return {
        link: function (scope, element, attrs) {
        	// Since the promise may not have reolved yet, we need a watcher.
        	scope.$watch('app.xavee_score', function(xavee_score) {
	        	if(xavee_score < 50) element.addClass("text-danger");
	    		else if(xavee_score < 80) element.addClass("text-warning");
	    		else element.addClass("text-success");
        	});
        }
    };
})

/**
 * Directive to give the Xavee score a color.
 */
.directive('developerScore', function () {
    return {
        link: function (scope, element, attrs) {
        	// Since the promise may not have reolved yet, we need a watcher.
        	scope.$watch('developer.xavee_score', function(xavee_score) {
	        	if(xavee_score < 50) element.addClass("text-danger");
	    		else if(xavee_score < 80) element.addClass("text-warning");
	    		else element.addClass("text-success");
        	});
        }
    };
})

/**
* Directive for a floating facet bar.
* The navigation bar will stick to the top of the browser window after we've scrolled past the main navigation bar.
*/
.directive('stickToTop', function () {
    return {
        link: function (scope, element, attrs) {	
        	// Get initial top offset of the facet bar.
        	var floatingNavigationOffsetTop = $('#facetbar').offset().top;

        	// Define the floating navigation function.
        	var floatingNavigation = function() {
        		// current vertical position from the top.
        		var scrollTop = $(window).scrollTop();
        		
    			// Current height of the facet bar. This is variable as elements may stack.
    			var navSize = $('#facetbar').height();
        		
        		// If scrolled more than the navigation, change position
        		// from static to fixed in order to float-to-top.
        		if (scrollTop > floatingNavigationOffsetTop) {
        			$('#facetbar').removeClass('navbar-static-top').addClass('navbar-fixed-top');
        			$('#content').css('padding-top', (navSize - 35) + 'px');
        		} else {
        			$('#facetbar').removeClass('navbar-fixed-top').addClass('navbar-static-top');
        			$('#content').css('padding-top', '0');
        		}
        	}

        	// Run function on load.
        	floatingNavigation();

        	// Run function every time you scroll.
        	$(window).scroll(floatingNavigation);
        }
    };
});
