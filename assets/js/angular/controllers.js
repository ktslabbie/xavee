/** 
 * Created on May 18, 2014
 * 
 * @author Kristian
 * 
 * File for Angular.js controllers.
 */

var xaveeController = angular.module('xavee.controller', []);

xaveeController.controller('PostController', ['$scope', 'Post', function($scope, Post) {
	$scope.posts = Post.query();
}]);

xaveeController.controller('ApplicationController', ['$scope', 'Application', function($scope, Application) {
	$scope.apps = Application.apps();
}]);

xaveeController.controller('ApplicationDetailController', ['$scope', 'Application', function($scope, Application, AppID) {
	
	$scope.app = Application.apps({id:AppID.getID()});
	
}]);

// Controller for the Ranking page.
xaveeController.controller('RankingController', ['$scope', 'Ranking', function($scope, Ranking, AppID) {
	
	countries = [                                                                                                                                                                                                 
		['us', 'United States'],                                                                                                                                                                                                                         
		['jp', 'Japan'],                                                                                                                                                                                                                         
		['gb', 'United Kingdom'],
		['de', 'Germany'],
		['fr', 'France'],
		['kr', 'South Korea'],
		['au', 'Australia'],
		['cn', 'China'],
		['ca', 'Canada'],
		['es', 'Spain'],
		['it', 'Italy'],
		['ru', 'Russia'],
		['nl', 'The Netherlands'],
	];
	
	$scope.categories = [
	    {id:-1,   genre:'All Applications', type:'Applications'},
	    {id:6000, genre:'Business', type:'Applications'},
	    {id:6001, genre:'Weather', type:'Applications'},
	    {id:6002, genre:'Utilities', type:'Applications'},
	    {id:6003, genre:'Travel', type:'Applications'},
	    {id:6004, genre:'Sports', type:'Applications'},
	    {id:6005, genre:'Social Networking', type:'Applications'},
	    {id:6006, genre:'Reference', type:'Applications'},
	    {id:6007, genre:'Productivity', type:'Applications'},
	    {id:6008, genre:'Photo & Video', type:'Applications'},
	    {id:6009, genre:'News', type:'Applications'},
	    {id:6010, genre:'Navigation', type:'Applications'},
	    {id:6011, genre:'Music', type:'Applications'},
	    {id:6012, genre:'Lifestyle', type:'Applications'},
	    {id:6013, genre:'Health & Fitness', type:'Applications'},
	    {id:6014, genre:'All Games', type:'Games'},
	    	{id:7001, genre:'Action', type:'Games'},
	    	{id:7002, genre:'Adventure', type:'Games'},
	    	{id:7003, genre:'Arcade', type:'Games'},
	    	{id:7004, genre:'Board', type:'Games'},
	    	{id:7005, genre:'Card', type:'Games'},
	    	{id:7006, genre:'Casino', type:'Games'},
	    	{id:7007, genre:'Dice', type:'Games'},
	    	{id:7008, genre:'Educational', type:'Games'},
	    	{id:7009, genre:'Family', type:'Games'},
	    	{id:7010, genre:'Kids', type:'Games'},
	    	{id:7011, genre:'Music', type:'Games'},
	    	{id:7012, genre:'Puzzle', type:'Games'},
	    	{id:7013, genre:'Racing', type:'Games'},
	    	{id:7014, genre:'Role Playing', type:'Games'},
	    	{id:7015, genre:'Simulation', type:'Games'},
	    	{id:7016, genre:'Sports', type:'Games'},
	    	{id:7017, genre:'Strategy', type:'Games'},
	    	{id:7018, genre:'Trivia', type:'Games'},
	    	{id:7019, genre:'Word', type:'Games'},
	    {id:6015, genre:'Finance', type:'Applications'},
	    {id:6016, genre:'Entertainment', type:'Applications'},
	    {id:6017, genre:'Education', type:'Applications'},
	    {id:6018, genre:'Books', type:'Applications'},
	    {id:6020, genre:'Medical', type:'Applications'},
	    {id:6021, genre:'Newsstand', type:'Applications'},
	    {id:6022, genre:'Catalogs', type:'Applications'},
 	];
	
	$scope.platformButton = 'iphone';
	$scope.rankingTypeButton = '1';
	$scope.countryButton = 'us';
	$scope.activeCategory = $scope.categories[0];
	$scope.countries = countries;
	$scope.selected = 0;
	
	$scope.ranking = Ranking.ranking({country:$scope.countryButton, ranking_type:$scope.rankingTypeButton, category:$scope.activeCategory.id});
	
	$scope.sendID = function(id) {
		AppID.setID(id);
	}
	
	$scope.changeRankingType = function(rankingType) {
		$scope.rankingTypeButton = rankingType;
		$scope.ranking = Ranking.ranking({country:$scope.countryButton, ranking_type:$scope.rankingTypeButton, category:$scope.activeCategory.id});
		
	};
	
	$scope.changeCountry = function(country, index) {
		$scope.countryButton = country;
		$scope.selected = index;
		$scope.ranking = Ranking.ranking({country:$scope.countryButton, ranking_type:$scope.rankingTypeButton, category:$scope.activeCategory.id});
	};
	
	$scope.changeCategory = function(category) {
		$scope.activeCategory = category;
		$scope.ranking = Ranking.ranking({country:$scope.countryButton, ranking_type:$scope.rankingTypeButton, category:$scope.activeCategory.id});
	};
}]);

// Controller for the rankings per version.
xaveeController.controller('VersionRankingController', ['$scope', 'VersionRanking', function($scope, VersionRanking) {
	$scope.versionRank = VersionRanking.versionRanking({application_id:$scope.rank.version.application.id, ranking_type:$scope.rankingTypeButton});
	
//	$scope.getVersions = function() {
//		return versionRank;
//	};
}]);
	