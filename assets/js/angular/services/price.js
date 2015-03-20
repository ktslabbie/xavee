/** 
 * Created on January 4, 2015
 * 
 * @author Kristian
 * 
 * Service to get the price in the right currency.
 */
var priceService = angular.module('service.price', [])

.factory('Price', ['$translate', function($translate) {
	
	// The string to be translated for free apps.
	var free;
	
	// Always executed once when changing languages.
	$translate(['FREE',]).then(function (translations) {
		free = translations.FREE;
	});
	
	return {
		getPrice: function(currency, price) {
			if(parseFloat(price) == 0) return free;

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
    	},
    }
}]);