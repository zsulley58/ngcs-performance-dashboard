import pandas as pd
import random
from datetime import datetime
import os


def fetch_real_time_data():
    # Simulate fetching real-time data
    data = {
        'timestamp': [datetime.now()],
        'pressure': [random.uniform(50, 100)],
        'temperature': [random.uniform(20, 40)],
        'flow_rate': [random.uniform(10, 30)]
    }
    df = pd.DataFrame(data)
    return df


if __name__ == "__main__":
    data_dir = os.path.join(os.path.dirname(__file__), '../data')
    file_path = os.path.join(data_dir, 'real_time_data.xlsx')

    new_data = fetch_real_time_data()
    try:
        # Read the existing data from the provided Excel file
        existing_data = pd.read_excel(file_path, engine='openpyxl')
        # Append new data to the existing data
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
    except FileNotFoundError:
        # If the file doesn't exist, start with the new data
        updated_data = new_data

    # Save the updated data back to the Excel file
    updated_data.to_excel(file_path, index=False)
