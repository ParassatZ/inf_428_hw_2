import numpy as np
import unittest

def generate_random_data(mean, variance, num_samples):
    return np.random.randint(max(mean - variance, 0), min(mean + variance + 1, 90), num_samples)

def calculate_aggregated_threat_score(departments, importance, num_users):
    weighted_scores = []
    total_weights = 0
    for i, dept_scores in enumerate(departments):
        weight = importance[i] * num_users[i]
        avg_dept_score = np.mean(dept_scores)
        weighted_scores.append(avg_dept_score * weight)
        total_weights += weight
    return sum(weighted_scores) / total_weights

class TestAggregatedThreatScore(unittest.TestCase):
    
    def test_equal_departments(self):
        departments = [generate_random_data(45, 10, 50) for _ in range(5)]
        importance = [3, 3, 3, 3, 3]
        num_users = [50, 50, 50, 50, 50]
        aggregated_score = calculate_aggregated_threat_score(departments, importance, num_users)
        self.assertTrue(0 <= aggregated_score <= 90)
        print(aggregated_score)

    def test_varying_importance(self):
        departments = [generate_random_data(45, 10, 50) for _ in range(5)]
        importance = [1, 2, 3, 4, 5]
        num_users = [50, 50, 50, 50, 50]
        aggregated_score = calculate_aggregated_threat_score(departments, importance, num_users)
        self.assertTrue(0 <= aggregated_score <= 90)
        print(aggregated_score)

    def test_outliers(self):
        departments = [
            generate_random_data(45, 10, 50),
            generate_random_data(80, 5, 50),  # high outlier
            generate_random_data(5, 5, 50),   # low outlier
            generate_random_data(45, 10, 50),
            generate_random_data(45, 10, 50)
        ]
        importance = [3, 3, 3, 3, 3]
        num_users = [50, 50, 50, 50, 50]
        aggregated_score = calculate_aggregated_threat_score(departments, importance, num_users)
        self.assertTrue(0 <= aggregated_score <= 90)
        print(aggregated_score)

    def test_different_user_counts(self):
        departments = [generate_random_data(45, 10, num) for num in [10, 20, 30, 150, 200]]
        importance = [3, 3, 3, 3, 3]
        num_users = [10, 20, 30, 150, 200]
        aggregated_score = calculate_aggregated_threat_score(departments, importance, num_users)
        self.assertTrue(0 <= aggregated_score <= 90)
        print(aggregated_score)

if __name__ == "__main__":
    unittest.main()