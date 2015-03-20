/** 
 * Created on May 18, 2014
 * 
 * @author Kristian
 * 
 * Controller for the facetbar. This needs access to ranking types, coutries, categories, etc.
 */
var facetbarCtrl = angular.module('ctrl.facetbar', [])

.controller('FacetbarCtrl', ['$scope', '$location', 'Rankings', 'Countries', 'RankingTypes', 'Categories', 
                                   function($scope, $location, Rankings, Countries, RankingTypes, Categories) {
	
	$scope.rankings = CONSTS.rankings;
	$scope.countryLists = CONSTS.countryLists;
	$scope.rankingTypeLists = CONSTS.rankingTypeLists;
	$scope.categories = CONSTS.categories;
	
	// Place some required service functions on the scope.
	// We need to include the entire functions to enable two-way binding.
	$scope.getActiveRanking = Rankings.getActiveRanking;
	$scope.getActiveCountry = Countries.getActiveCountry;
	$scope.getActiveRankingType = RankingTypes.getActiveRankingType;
	$scope.getActiveRankingTypeList = RankingTypes.getActiveRankingTypeList;
	$scope.getActiveCategory = Categories.getActiveCategory;
	
	// Update the active ranking and the URL.
	$scope.changeRanking = function(ranking) {
		Rankings.setActiveRanking(ranking);
		if($scope.getActiveRankingType() != 'free' && $scope.getActiveRankingType() != 'paid') RankingTypes.setActiveRankingType('free');
		RankingTypes.setActiveRankingTypeList(ranking.split('-')[0]);
		updatePage();
	}
	
	// Update the active country and the URL.
	$scope.changeCountry = function(country) {
		Countries.setActiveCountry(country);
		updatePage();
	}
	
	// Update the active world ranking type and the URL.
	$scope.changeRankingType = function(rankingType) {
		RankingTypes.setActiveRankingType(rankingType);
		updatePage();
	}
	
	// Update the active category and the URL.
	$scope.changeCategory = function(category) {
		Categories.setActiveCategory(category);
		updatePage();
	}
	
	// Update the page by URL rewriting.
	function updatePage() {
		if($scope.getActiveRankingType() == 'developers') {
			$location.url($scope.getActiveRanking() + "-rankings/" + $scope.getActiveCountry() + "/" + CONSTS.defaults.platform + "/" + 
					  $scope.getActiveRankingType() + "/" + $scope.getActiveCategory());
		} else {
			$location.url($scope.getActiveRanking() + "-rankings/" + $scope.getActiveCountry() + "/" + CONSTS.defaults.platform + "/" + 
					  $scope.getActiveRankingType() + "/" + $scope.getActiveCategory());
		}
		
	};
}]);