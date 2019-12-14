import unittest 
import main as webscrape
import os
from matplotlib import pyplot as plt
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
class SimpleTest(unittest.TestCase): 
  
    def testDataList(self):
        # webscrape.overall_states()
        if len(webscrape.states_name) ==0:
            self.fail("Could Not Fetch States Name")
        elif len(webscrape.states_abbr) ==0:
            self.fail("Could Not Fetch States Abbrevation")
        elif len(webscrape.capital) ==0:
            self.fail("Could Not Fetch States Capital")
        elif len(webscrape.established) ==0:
            self.fail("Could Not Fetch States Estabished Date")
        elif len(webscrape.population) ==0:
            self.fail("Could Not Fetch States population")
        elif len(webscrape.total_area) ==0:
            self.fail("Could Not Fetch States total area")
        elif len(webscrape.land_area) ==0:
            self.fail("Could Not Fetch States land area")
        elif len(webscrape.water_area) ==0:
            self.fail("Could Not Fetch States water area")
        else:
            self.assertTrue(True)
            self.assertFalse(False)
    def testOverallCacheData(self):
        data = webscrape.overall_states()
        if len(data)>0:
            self.assertTrue(True)
            self.assertFalse(False)
        else:
            self.fail("No Data is Coming")
    def testCheckAbrrLength(self):
        # webscrape.overall_states()
        for i in webscrape.states_abbr:
            if len(i)>2:
                self.fail("Abbrevation cannot be greater than two letters")
            else:
                self.assertTrue(True)
                self.assertFalse(False)
    def testPopTrendData(self):
        # webscrape.overall_states()
        data, head = webscrape.poptrend("AL")
        if len(data)>0:
            self.assertTrue(True)
            self.assertFalse(False)
        else:
            self.fail("POPTREND command not working as expected")
    def testPopStatsData(self):
        # webscrape.overall_states()
        data, head = webscrape.popstats("AL")
        if len(data)>0:
            self.assertTrue(True)
            self.assertFalse(False)
        else:
            self.fail("POPSTATS command not working as expected")
    def testValidAreaDetails(self):
        # webscrape.overall_states()
        if len(webscrape.total_area) == len(webscrape.land_area):
            if len(webscrape.land_area) == len(webscrape.water_area):
                self.assertTrue(True)
                self.assertFalse(False)
            else:
                self.fail("Water Area Counts are Not matching Land Area Counts")
        else:
            self.fail("Total Area Counts are not matching Land Area Counts")
    def testLinks(self):
        # webscrape.overall_states()
        for i in webscrape.states_name:
            url = 'https://en.wikipedia.org/wiki/' + i.replace(" ","_")
            
            page = urlopen(url)
            soup = bs(page,'lxml')
            if soup:
                self.assertTrue(True)
                self.assertFalse(False)
            else:
                self.fail("No Data Fetched from state " + i)
    
if __name__ == '__main__': 
    unittest.main()