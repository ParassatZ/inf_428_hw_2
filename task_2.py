import numpy as np
from gen_random import generate_random_data

def calculate_department_threat(department_scores):
    return max(department_scores)

def calculate_company_threat(departments):
    max_department_threat = max(calculate_department_threat(department["scores"]) for department in departments)
    avg_threat = np.mean([
        calculate_department_threat(department["scores"]) for department in departments
    ])
    
    weight_max = np.random.uniform(0.6, 0.8)  
    weight_avg = 1 - weight_max              

    company_threat_score = weight_max * max_department_threat + weight_avg * avg_threat
    return min(max(company_threat_score, 0), 90)  

if __name__ == "__main__":
    departments_data = [
        {"scores": generate_random_data(10, 5, 50)},
        {"scores": generate_random_data(70, 10, 100)},
        {"scores": generate_random_data(60, 15, 75)},
        {"scores": generate_random_data(20, 5, 80)},
        {"scores": generate_random_data(30, 10, 30)},
    ]

    company_threat_score = calculate_company_threat(departments_data)
    for department in departments_data:
        print("Department scores:", department["scores"])
    print("Final Company Threat Score:", company_threat_score)
