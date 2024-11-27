import os
import numpy as np
import time
import pandas as pd
from elasticsearch import Elasticsearch
from gen_random import generate_random_data


def get_es_client():
    es_host = os.getenv('ES_HOST', 'https://localhost:9200')  # Получаем адрес из переменной окружения, если он есть
    es = Elasticsearch(
        [es_host],  # Используем переменную es_host
        verify_certs=False  # Отключаем проверку сертификатов, если они самоподписанные
    )
    return es

# Функция для проверки доступности Elasticsearch
def wait_for_es(es_client, retries=10, delay=5):
    for _ in range(retries):
        try:
            if es_client.ping():
                print("Elasticsearch is up and running.")
                return True
            else:
                print("Elasticsearch is not responding, retrying...")
        except Exception as e:
            print(f"Error connecting to Elasticsearch: {e}, retrying...")
        time.sleep(delay)  
    print("Elasticsearch is not available after several attempts.")
    return False

# Функция для расчета угрозы по отделу
def calculate_department_threat(department_scores):
    return max(department_scores)

# Функция для расчета угрозы для всей компании
def calculate_company_threat(departments):
    max_department_threat = max(calculate_department_threat(department["scores"]) for department in departments)
    avg_threat = np.mean([calculate_department_threat(department["scores"]) for department in departments])
    
    weight_max = np.random.uniform(0.6, 0.8)  
    weight_avg = 1 - weight_max              

    company_threat_score = weight_max * max_department_threat + weight_avg * avg_threat
    return min(max(company_threat_score, 0), 90)  

# Функция для индексации данных в Elasticsearch
def index_data_to_es(departments_data):
    es = get_es_client()
    for i, department in enumerate(departments_data):
        doc = {
            'scores': department["scores"].tolist()
        }
        es.index(index="department_scores", id=i+1, document=doc)

# Функция для чтения данных из Elasticsearch
def read_data_from_es():
    es = get_es_client()
    result = es.search(index="department_scores", size=1000)
    return [{"scores": hit["_source"]["scores"]} for hit in result["hits"]["hits"]]

# Функция для генерации и сохранения данных в CSV
def save_data_to_csv():
    departments_data = [
        {"scores": generate_random_data(10, 5, 50)},
        {"scores": generate_random_data(70, 10, 100)},
        {"scores": generate_random_data(60, 15, 75)},
        {"scores": generate_random_data(20, 5, 80)},
        {"scores": generate_random_data(30, 10, 30)},
    ]
    df = pd.DataFrame([dep["scores"] for dep in departments_data])
    df.to_csv('data.csv', index=False)

# Главная функция
if __name__ == "__main__":
    es_client = get_es_client()
    if not wait_for_es(es_client):
        print("Exiting due to Elasticsearch not being available.")
        exit(1)

    # Сохраняем данные в CSV
    save_data_to_csv()

    # Загружаем данные из CSV
    df = pd.read_csv('data.csv')
    departments_data = [{"scores": row.tolist()} for row in df.values]

    # Индексируем данные в Elasticsearch
    index_data_to_es(departments_data)

    # Читаем данные из Elasticsearch
    departments_data_from_es = read_data_from_es()

    # Рассчитываем угроза для компании
    company_threat_score = calculate_company_threat(departments_data_from_es)
    
    for department in departments_data_from_es:
        print("Department scores:", department["scores"])
    print("Final Company Threat Score:", company_threat_score)
