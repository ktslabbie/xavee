/** 
 * Created on May 18, 2014
 * 
 * @author Kristian
 * 
 * File for the Angular.js base controller.
 */
var xaveeController = angular.module('xavee.base-controller', [])

// A Base controller that other controllers can extend.
.controller('BaseController', ['$scope', '$translate', 
                               function($scope, $translate) {

	$translate(['FREE',]).then(function (translations) {		
		$scope.getPrice = function(currency, price) {
			if(parseFloat(price) == 0) return translations.FREE;

			switch (currency) {
				case "USD":
				case "CAD":
				case "AUD":
					return "$" + price;
				case "JPY":
					return "¥" + parseFloat(price);
				case "EUR":
					return "€" + price;
				case "GBP":
					return "£" + price;
				case "RUB":
					return parseFloat(price) + " p.";
				case "CNY":
					return "¥" + parseFloat(price);
			}

			return currency + " " + price;
		}
	});
}]);