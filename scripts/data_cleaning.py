import pandas as pd
import os


def clean_data(df):
    # Handle missing values
    df = df.dropna()

    # Remove duplicates
    df = df.drop_duplicates()

    # Normalize data formats
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    return df


if __name__ == "__main__":
    data_dir = os.path.join(os.path.dirname(__file__), '../data')

    # Read and clean real-time data
    real_time_file_path = os.path.join(data_dir, 'real_time_data.xlsx')
    real_time_data = pd.read_excel(real_time_file_path, engine='openpyxl')
    clean_real_time_data = clean_data(real_time_data)
    clean_real_time_data.to_excel(os.path.join(
        data_dir, 'clean_real_time_data.xlsx'), index=False)

    # Read and clean historical data
    historical_file_path = os.path.join(data_dir, 'historical_data.xlsx')
    historical_data = pd.read_excel(historical_file_path, engine='openpyxl')
    clean_historical_data = clean_data(historical_data)
    clean_historical_data.to_excel(os.path.join(
        data_dir, 'clean_historical_data.xlsx'), index=False)
