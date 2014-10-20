/** 
 * Created on Sep 20, 2014
 * 
 * @author Kristian
 * 
 * File for Angular.js translation controllers.
 */
var xaveeController = angular.module('xavee.tl-controller', [])

.controller('TLController', ['$scope', '$translate', function($scope, $translate) {
	
	$translate(['US_NAME', 'JP_NAME', 'GB_NAME', 'DE_NAME', 'FR_NAME', 'KR_NAME', 'AU_NAME', 
	            'CN_NAME', 'CA_NAME', 'ES_NAME', 'IT_NAME', 'RU_NAME', 'NL_NAME',
	            'CAT_0', 'CAT_6000', 'CAT_6001', 'CAT_6002', 'CAT_6003', 'CAT_6004', 'CAT_6005', 'CAT_6006', 
	            'CAT_6007', 'CAT_6008', 'CAT_6009', 'CAT_6010', 'CAT_6011', 'CAT_6012', 'CAT_6013', 'CAT_6015',
	            'CAT_6016', 'CAT_6017', 'CAT_6018', 'CAT_6020', 'CAT_6021', 'CAT_6022', 'CAT_6023', 
	            'CAT_6014', 'CAT_7001', 'CAT_7002', 'CAT_7003', 'CAT_7004', 'CAT_7005', 'CAT_7006', 
	            'CAT_7007', 'CAT_7008', 'CAT_7009', 'CAT_7011', 'CAT_7012', 'CAT_7013',
	            'CAT_7014', 'CAT_7015', 'CAT_7016', 'CAT_7017', 'CAT_7018', 'CAT_7019', 
	
	]).then(function (translations) {
		
		$scope.countries = [ 
				{code: 'us', name: translations.US_NAME},
				{code: 'jp', name: translations.JP_NAME},
				{code: 'gb', name: translations.GB_NAME},
				{code: 'de', name: translations.DE_NAME},
				{code: 'fr', name: translations.FR_NAME},
				{code: 'kr', name: translations.KR_NAME},
				{code: 'au', name: translations.AU_NAME},
				{code: 'cn', name: translations.CN_NAME},
				{code: 'ca', name: translations.CA_NAME},
				{code: 'es', name: translations.ES_NAME},
				{code: 'it', name: translations.IT_NAME},
				{code: 'ru', name: translations.RU_NAME},
				{code: 'nl', name: translations.NL_NAME}
		];
		
		$scope.appCategories = [
	        	{id:0,    genre:translations.CAT_0},
	        	{id:6000, genre:translations.CAT_6000},
	        	{id:6001, genre:translations.CAT_6001},
	        	{id:6002, genre:translations.CAT_6002},
	        	{id:6003, genre:translations.CAT_6003},
	        	{id:6004, genre:translations.CAT_6004},
	        	{id:6005, genre:translations.CAT_6005},
	        	{id:6006, genre:translations.CAT_6006},
	        	{id:6007, genre:translations.CAT_6007},
	        	{id:6008, genre:translations.CAT_6008},
	        	{id:6009, genre:translations.CAT_6009},
	        	{id:6010, genre:translations.CAT_6010},
	        	{id:6011, genre:translations.CAT_6011},
	        	{id:6012, genre:translations.CAT_6012},
	        	{id:6013, genre:translations.CAT_6013},
	        	{id:6015, genre:translations.CAT_6015},
	        	{id:6016, genre:translations.CAT_6016},
	        	{id:6017, genre:translations.CAT_6017},
	        	{id:6018, genre:translations.CAT_6018},
	        	{id:6020, genre:translations.CAT_6020},
	        	{id:6021, genre:translations.CAT_6021},
	        	{id:6022, genre:translations.CAT_6022},
	        	{id:6023, genre:translations.CAT_6023},
		 ];
		
		$scope.gameCategories = [
	        	{id:6014, genre:translations.CAT_6014},
	        	{id:7001, genre:translations.CAT_7001},
	        	{id:7002, genre:translations.CAT_7002},
	        	{id:7003, genre:translations.CAT_7003},
	        	{id:7004, genre:translations.CAT_7004},
	        	{id:7005, genre:translations.CAT_7005},
	        	{id:7006, genre:translations.CAT_7006},
	        	{id:7007, genre:translations.CAT_7007},
	        	{id:7008, genre:translations.CAT_7008},
	        	{id:7009, genre:translations.CAT_7009},
	        	{id:7011, genre:translations.CAT_7011},
	        	{id:7012, genre:translations.CAT_7012},
	        	{id:7013, genre:translations.CAT_7013},
	        	{id:7014, genre:translations.CAT_7014},
	        	{id:7015, genre:translations.CAT_7015},
	        	{id:7016, genre:translations.CAT_7016},
	        	{id:7017, genre:translations.CAT_7017},
	        	{id:7018, genre:translations.CAT_7018},
	        	{id:7019, genre:translations.CAT_7019},
		 ];
	});
}]);