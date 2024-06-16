import pandas as pd


def extract_historical_data(file_path):
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
        # Perform some basic validation
        if df.isnull().values.any():
            print("Data contains missing values.")
            df = df.dropna()
        print("Historical data extracted successfully.")
        return df
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None


if __name__ == "__main__":
    historical_data = extract_historical_data('data/historical_data.xlsx')
    if historical_data is not None:
        historical_data.to_excel(
            'data/processed_historical_data.xlsx', index=False)
