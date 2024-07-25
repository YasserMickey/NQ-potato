import pandas as pd
from IPython.display import display


# Load the dataset
file_path = 'NQ_daily_nearby_badj.csv'
data = pd.read_csv(file_path)


# Convert the 'Time' column to datetime format
data['Time'] = pd.to_datetime(data['Time'], format='%m/%d/%Y')

# Filter data for the years 2019 to 2023
data_filtered = data[data['Time'].dt.year.between(2019, 2023)].copy()

# Ensure the 'Week' column is recalculated
data_filtered.loc[:, 'Week'] = data_filtered['Time'].dt.isocalendar().week

# Calculate the total number of weeks for each year
data_filtered.loc[:, 'Year'] = data_filtered['Time'].dt.year
weeks_per_year = data_filtered.groupby('Year')['Week'].nunique()

def calculate_highs_lows(data, value_col):
    results = pd.DataFrame()

    for year in range(2019, 2023 + 1):
        data_year = data[data['Year'] == year].copy()
        data_year.loc[:, 'Week'] = data_year['Time'].dt.isocalendar().week
        data_year.loc[:, 'DayOfWeek'] = data_year['Time'].dt.day_name()

        if value_col == 'High':
            weekly_values = data_year.groupby('Week')['High'].idxmax()
        else:
            weekly_values = data_year.groupby('Week')['Low'].idxmin()

        days_with_values = data_year.loc[weekly_values, 'DayOfWeek'].value_counts()
        results[year] = days_with_values

    results = results.fillna(0).astype(int)
    formatted_results = []

    for year in results.columns:
        max_day = results[year].idxmax()
        max_count = results[year].max()
        formatted_results.append({'Year': year, 'Day': max_day, 'Count': max_count})

    formatted_results_df = pd.DataFrame(formatted_results)
    formatted_results_df = formatted_results_df.merge(weeks_per_year, left_on='Year', right_index=True)
    formatted_results_df.rename(columns={'Week': 'TotalWeeks'}, inplace=True)
    formatted_results_df['Percentage'] = (formatted_results_df['Count'] / formatted_results_df['TotalWeeks']) * 100
    formatted_results_df = formatted_results_df[['Year', 'Day', 'Count', 'Percentage']]
    formatted_results_df['Percentage'] = formatted_results_df['Percentage'].round(1).astype(str) + '%'

    return formatted_results_df

# Calculate highs and lows
highs_df = calculate_highs_lows(data_filtered, 'High')
lows_df = calculate_highs_lows(data_filtered, 'Low')

# Display the results
print("Weekly Highest Days from 2019 to 2023")
display(highs_df)
print("\nWeekly Lowest Days from 2019 to 2023")
display(lows_df)

