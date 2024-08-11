import pandas as pd

# Read the CSV file
lightning_df = pd.read_csv(r"exel\all data filtered.csv")

# Convert DATE AND TIME column to datetime format
lightning_df['Datetime'] = pd.to_datetime(lightning_df['DATE AND TIME'], format='%Y%m%dT%H%M%S.%f')

# Drop the original DATE AND TIME column if needed
lightning_df.drop(columns=['DATE AND TIME'], inplace=True)


# Create a new column 'year-month'
lightning_df['year-month'] = lightning_df['Datetime'].dt.strftime('%Y-%m')
lightning_df['time'] = lightning_df['Datetime'].dt.strftime('%H:%M:%S.%f').str[:-4]

# Drop the Datetime column
lightning_df.drop(columns=['Datetime'], inplace=True)


# Group the DataFrame by 'year-month' and create a dictionary of DataFrames
dfs_by_month = {}
for name, group in lightning_df.groupby('year-month'):
    dfs_by_month[name] = group

# Access DataFrames by month and save each to a separate CSV file
for month, df_month in dfs_by_month.items():
    print("Month:", month)
    print(df_month)
    df_month.to_csv(fr'exel\months df\{month}.csv', index=False)
    print()

