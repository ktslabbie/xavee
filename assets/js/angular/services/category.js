/** 
 * Created on January 4, 2015
 * 
 * @author Kristian
 * 
 * Service to keep track of the currently active category.
 */
var categoryService = angular.module('service.category', [])

.factory('Categories', function() {
	
	// The currently active category.
    var activeCategory = 6014;
    
    return {
    	setActiveCategory: function(category) {
    		activeCategory = category;
    	},
        
        getActiveCategory: function() { return activeCategory },
    }
});