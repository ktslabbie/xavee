var CONSTS = {
		
		// Application defaults.
		defaults: {
			ranking: 'world',
			platform: "iphone",
			country: 'us',
			rankingType: 'free',
			rankingTypeList: 'world',
			category: 6014
		},
		
		rankings: [ 'world', 'xavee' ],
		
		// Country lists per active language.
	    // English users will be more interested in English-language countries, so put those ahead.
	    countryLists: {
			en: [ 'us', 'jp', 'gb', 'de', 'fr', 'kr', 'au', 'cn', 'ca', 'es', 'it', 'ru', 'nl', ],
			ja: [ 'jp', 'us', 'kr', 'gb', 'de', 'fr', 'au', 'cn', 'ca', 'es', 'it', 'ru', 'nl', ],
		},
		
		// A list of ranking types currently supported. World ranking types taken from the iTunes store.
		rankingTypeLists: {
			world: [ 'free', 'paid', 'grossing' ],
			xavee: [ 'free', 'paid', 'developers' ],
		},
				
		// A list of the categories currently supported. IDs taken from iTunes categories.
		categories: [ 6014, 7001, 7002, 7003, 7004, 7005, 7006, 7007, 7008, 7009, 7011, 7012, 7013, 7014, 7015, 7016, 7017, 7018, 7019 ],
		
		// Simple map to get the country code for the supported languages.
		langToCountry: { en: 'us', ja: 'jp' },
}
