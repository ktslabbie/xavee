# -*- coding: utf-8 -*-
'''
Created on Aug 6, 2014

@author: Kristian
'''
from selenium import webdriver
import unittest

class testNewVisitor(unittest.TestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox() 
        self.browser.implicitly_wait(3)
        
    def tearDown(self):
        self.browser.quit()
    
    def testViewBlogList(self):
        # User opens the browser and goes the the Xavee homepage.
        self.browser.get('http://localhost:8000/')
        
        # Check that the right title is displayed in the title bar.
        self.assertIn('Xavee', self.browser.title)
        
        # Note that there are currently 4 possible pages in the navbar.
        
        
        #self.fail("Finish the tests!")
        
        

if __name__ == '__main__':
    unittest.main()