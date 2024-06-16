import pandas as pd
from datetime import datetime, timedelta
import random
import os

# Generate sample historical data


def generate_sample_data(num_days=30):
    base = datetime.today()
    date_list = [base - timedelta(days=x) for x in range(num_days)]
    data = {
        'timestamp': date_list,
        'pressure': [random.uniform(50, 100) for _ in range(num_days)],
        'temperature': [random.uniform(20, 40) for _ in range(num_days)],
        'flow_rate': [random.uniform(10, 30) for _ in range(num_days)]
    }
    df = pd.DataFrame(data)
    return df


if __name__ == "__main__":
    data_dir = os.path.join(os.path.dirname(__file__), '../data')
    os.makedirs(data_dir, exist_ok=True)
    sample_data = generate_sample_data()
    sample_data.to_excel(os.path.join(
        data_dir, 'historical_data.xlsx'), index=False)
