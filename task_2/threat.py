import numpy as np
import unittest

def generate_random_data(mean, variance, num_samples):
    lower_bound = max(mean - variance, 0)
    upper_bound = min(mean + variance, 90)
    if lower_bound >= upper_bound:
        raise ValueError("Invalid mean or variance: bounds overlap")
    return np.random.randint(lower_bound, upper_bound + 1, num_samples)

def calculate_aggregated_threat_score(departments, importance, num_users):
    
    if not (len(departments) == len(importance) == len(num_users)):
        raise ValueError("Mismatch in lengths of departments, importance, and num_users")
    
    weighted_scores = []
    total_weights = 0
    for i, dept_scores in enumerate(departments):
        weight = importance[i] * num_users[i]
        avg_dept_score = np.mean(dept_scores)
        weighted_scores.append(avg_dept_score * weight)
        total_weights += weight
    
    if total_weights == 0:  
        return 0
    return sum(weighted_scores) / total_weights

class TestAggregatedThreatScore(unittest.TestCase):
    
    def test_equal_departments(self):
        np.random.seed(42)  
        departments = [generate_random_data(45, 10, 50) for _ in range(5)]
        importance = [3, 3, 3, 3, 3]
        num_users = [50, 50, 50, 50, 50]
        aggregated_score = calculate_aggregated_threat_score(departments, importance, num_users)
        print(f"Test Equal Departments: {aggregated_score}")
        self.assertTrue(0 <= aggregated_score <= 90)

    def test_varying_importance(self):
        np.random.seed(42)
        departments = [generate_random_data(45, 10, 50) for _ in range(5)]
        importance = [1, 2, 3, 4, 5]
        num_users = [50, 50, 50, 50, 50]
        aggregated_score = calculate_aggregated_threat_score(departments, importance, num_users)
        print(f"Test Varying Importance: {aggregated_score}")
        self.assertTrue(0 <= aggregated_score <= 90)

    def test_outliers(self):
        np.random.seed(42)
        departments = [
            generate_random_data(45, 10, 50),
            generate_random_data(80, 5, 50),  
            generate_random_data(5, 5, 50),   
            generate_random_data(45, 10, 50),
            generate_random_data(45, 10, 50)
        ]
        importance = [3, 3, 3, 3, 3]
        num_users = [50, 50, 50, 50, 50]
        aggregated_score = calculate_aggregated_threat_score(departments, importance, num_users)
        print(f"Test Outliers: {aggregated_score}")
        self.assertTrue(0 <= aggregated_score <= 90)

    def test_different_user_counts(self):
        np.random.seed(42)
        departments = [generate_random_data(45, 10, num) for num in [10, 20, 30, 150, 200]]
        importance = [3, 3, 3, 3, 3]
        num_users = [10, 20, 30, 150, 200]
        aggregated_score = calculate_aggregated_threat_score(departments, importance, num_users)
        print(f"Test Different User Counts: {aggregated_score}")
        self.assertTrue(0 <= aggregated_score <= 90)

    def test_empty_departments(self):
        departments = []
        importance = []
        num_users = []
        result = calculate_aggregated_threat_score(departments, importance, num_users)
        print(f"Test Empty Departments: {result}")
        self.assertEqual(result, 0)

    def test_zero_users(self):
        np.random.seed(42)
        departments = [generate_random_data(45, 10, 50) for _ in range(5)]
        importance = [3, 3, 3, 3, 3]
        num_users = [0, 0, 0, 0, 0]  
        result = calculate_aggregated_threat_score(departments, importance, num_users)
        print(f"Test Zero Users: {result}")
        self.assertEqual(result, 0)

    def test_extreme_weights(self):
        np.random.seed(42)
        departments = [generate_random_data(45, 10, 50) for _ in range(5)]
        importance = [0, 0, 5, 0, 0]  
        num_users = [0, 0, 200, 0, 0]  
        result = calculate_aggregated_threat_score(departments, importance, num_users)
        print(f"Test Extreme Weights: {result}")
        self.assertTrue(0 <= result <= 90)

if __name__ == "__main__":
    unittest.main()
