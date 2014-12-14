"""
Created on Dec 5, 2014

This module handles Xavee rating calculation.

@author: Kristian
"""
class XaveeScore():
    """
    Utility class for calculating the Xavee score.
    """
    
    # Prior for the average of the bayesian rating. We gravitate toward this number.
    m = 2.75
    
    # Prior for the average of the Xavee rating. We gravitate toward this number.
    xm = 50
    
    # Confidence in the prior. The higher the number, the more ratings it will take to get away from it.
    # This can be variable, and controls how popular an app needs to be for the rating to be "right." 
    C = 200
    
    def set_bayesian_params(self, pm, pc):
        self.m = pm
        self.C = pc
    
    def get_bayesian_average(self, rating, rating_count):
        """ Returns the Bayesian average given the (average) rating and the number of ratings. """
        return round( ( self.C*self.m + float(rating)*rating_count ) / ( self.C + rating_count ) , 2)
    
    def get_xavee_score(self, rating, rating_count):
        """ Returns the Xavee score given the (average) rating and the number of ratings. """
        if rating is None or rating_count is None:
            # We can't judge the quality due to lack of ratings. Return the prior.
            return self.xm
        
        return int( (self.get_bayesian_average(float(rating), rating_count) - 1)*25 )
    
