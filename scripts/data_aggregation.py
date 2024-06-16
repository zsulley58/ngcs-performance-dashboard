import pandas as pd
import os


def aggregate_data(df, freq='H'):
    # Set the timestamp column as the index
    df.set_index('timestamp', inplace=True)

    # Resample the data based on the given frequency
    aggregated_data = df.resample(freq).mean()

    return aggregated_data.reset_index()


if __name__ == "__main__":
    data_dir = os.path.join(os.path.dirname(__file__), '../data')

    # Read and aggregate cleaned real-time data
    clean_real_time_file_path = os.path.join(
        data_dir, 'clean_real_time_data.xlsx')
    clean_real_time_data = pd.read_excel(
        clean_real_time_file_path, engine='openpyxl')
    aggregated_real_time_data = aggregate_data(clean_real_time_data, freq='H')
    aggregated_real_time_data.to_excel(os.path.join(
        data_dir, 'aggregated_real_time_data.xlsx'), index=False)

    # Read and aggregate cleaned historical data
    clean_historical_file_path = os.path.join(
        data_dir, 'clean_historical_data.xlsx')
    clean_historical_data = pd.read_excel(
        clean_historical_file_path, engine='openpyxl')
    aggregated_historical_data = aggregate_data(
        clean_historical_data, freq='D')
    aggregated_historical_data.to_excel(os.path.join(
        data_dir, 'aggregated_historical_data.xlsx'), index=False)
