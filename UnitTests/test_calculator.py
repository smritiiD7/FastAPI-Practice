import unittest
import calculator

class TestCalculator(unittest.TestCase):
    def test_add_functionality(self):
        result = calculator.cal_add(18,20)
        self.assertEqual(result, 38)
        
    def test_add_functionality_two_negative_number(self):
        result = calculator.cal_add(-10, -20)
        self.assertEqual(result, -30)