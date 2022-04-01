import pandas as pd

# Download media tracking file as .xlsx and convert to .csv
read_file = pd.read_excel('data/2021 GW Media Tracking.xlsx', sheet_name='media_tracking', engine='openpyxl')
read_file.to_csv('data/2021 GW Media Tracking.csv', index = None, header=True)

print(read_file.head())