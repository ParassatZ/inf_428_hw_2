import unittest
from task_2 import calculate_company_threat
from gen_random import generate_random_data

class TestCompanyThreatScore(unittest.TestCase):
    def test_similar_threat_scores(self):
        departments = [
            {"scores": generate_random_data(30, 5, 50)},
            {"scores": generate_random_data(30, 5, 50)},
            {"scores": generate_random_data(30, 5, 50)},
        ]
        result = calculate_company_threat(departments)
        print(f"Test Similar Threat Scores: result = {result}")
        self.assertTrue(0 <= result <= 90)

    def test_high_threat_in_one_department(self):
        departments = [
            {"scores": generate_random_data(20, 5, 50)},
            {"scores": generate_random_data(80, 5, 50)},
        ]
        result = calculate_company_threat(departments)
        print(f"Test High Threat in One Department: result = {result}")
        self.assertTrue(result > 40)

    def test_high_user_threat_in_one_department(self):
        departments = [
            {"scores": [10] * 49 + [90]},  
            {"scores": [30] * 50},         
        ]
        result = calculate_company_threat(departments)
        print(f"Test High User Threat in One Department: result = {result}")
        self.assertTrue(40 <= result <= 90)

    def test_dominant_department(self):
        departments = [
            {"scores": generate_random_data(10, 5, 50)},
            {"scores": generate_random_data(90, 5, 100)},  
            {"scores": generate_random_data(20, 5, 75)},
        ]
        result = calculate_company_threat(departments)
        print(f"Test Dominant Department: result = {result}")
        self.assertTrue(60 <= result <= 90)

    def test_different_user_counts(self):
        departments = [
            {"scores": generate_random_data(30, 5, 100)},  
            {"scores": generate_random_data(50, 10, 10)},  
        ]
        result = calculate_company_threat(departments)
        print(f"Test Different User Counts: result = {result}")
        self.assertTrue(0 <= result <= 90)

    def test_boundaries(self):
        departments_all_zero = [{"scores": [0] * 50}]
        departments_all_max = [{"scores": [90] * 50}]
        
        result_zero = calculate_company_threat(departments_all_zero)
        result_max = calculate_company_threat(departments_all_max)
        print(f"Test Boundaries (All Zero): result = {result_zero}")
        print(f"Test Boundaries (All Max): result = {result_max}")
        
        self.assertEqual(result_zero, 0)
        self.assertEqual(result_max, 90)

if __name__ == '__main__':
    unittest.main()
