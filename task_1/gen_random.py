import numpy as np

def generate_random_data(mean, variance, num_samples):
    low = max(mean - variance, 0)
    high = min(mean + variance + 1, 90)

    if low >= high:
        return np.full(num_samples, mean)

    data = np.random.randint(low, high, num_samples)
    if np.random.random() > 0.5:
        extreme_value = np.random.randint(0, 90)
        data[np.random.randint(0, len(data))] = extreme_value

    return data

