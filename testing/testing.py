import unittest

class TestCalculator(unittest.TestCase):
 
    def api_response(self,weekday,resultCounts):
        if (0 <= weekday < 5): 
            if resultCounts>0: return "data_loaded" 
            else: return "no_market_ops_day"
        else: return "weekend"
  
    def test_a(self):  
        self.assertEqual(self.api_response(2,10),"data_loaded")

    def test_b(self):    
        self.assertEqual(self.api_response(5,0),"weekend")
    
    def test_c(self):    
        self.assertEqual(self.api_response(3,0),"no_market_ops_day")
     
if __name__ == "__main__":
    unittest.main()