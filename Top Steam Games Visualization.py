# Importing Essential Libraries
# Such as Panda for Data Manipulation
# MatplotLib for Plotting Graphs
# and Seaborn for Statistical Data Visualization

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------------------------------------------------------------------------------------------------------------

# Import Data from a CSV File
# Data is From Kaggle Dataset of Top Steam Games
# https://www.kaggle.com/datasets/patelris/steam-top-1495-games-dataset

# Df is Data Frame and it uses the panda read function to read the csv file and storing it.
df = pd.read_csv('steam_top_games_2026.csv')

# Sea Born theme for the chart
sns.set_theme(style="whitegrid")

# Data Cleaning and Processing Section

# Pre processing the data by converting the release date column to a date time format. Which helps visualize the data when the game is released, and coerece to handle any errors.
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')

# Handle Missing Information by filling them with "Unknown" to avoid issues and breaking the charts.
df['developer'] = df['developer'].fillna('Unknown') # Unknown Dev
df['genres'] = df['genres'].fillna('Unknown') # Unknown Genre

# Custom function to turn owners of the game ranges like "1,000,000 .. 2,000,000" into numbers
# Because the dataset has the estimated_owners column in a range format instead of an integer, so we need to extract the range and convert it into a number(int)
def extract_owners(owner_str):
    if pd.isna(owner_str): return 0
    try:
        # Split by the ".." and take the first part, remove commas, and make it an integer
        lower_bound = owner_str.split(' .. ')[0].replace(',', '')
        return int(lower_bound)
    except:
        return 0

# Apply the function to the estimated Owners column
df['estimated_owners_lower'] = df['estimated_owners'].apply(extract_owners)

# Create a "clean" copy of the data without rows where the date was invalid
# Because some release dates are missing or invalid, so we create a cleaner version of the data frame that only includes rows with proper and valid release dates.
df_clean = df.dropna(subset=['release_date']).copy()
df_clean['release_year'] = df_clean['release_date'].dt.year

# ------------------------------------------------------------------------------------------------------------------------
# Graph Visualizations Section

# Graph 1: Distribution of Game Prices (Histogram Plot)
# This Histplot shows how much these games costs on steam and how many games fall into each price range.
# We filtered out the games that are under 100$ to avoid long tails on the chart, which can make it harder to see the distribution.
plt.figure(figsize=(10, 6))
# Filter to games under $100 to avoid long "tails" on the chart
sns.histplot(df_clean[df_clean['price_usd'] < 100]['price_usd'], bins=30, kde=True, color='skyblue')
# Title and Labels for the chart
plt.title('How much do games cost? (Price Distribution)')
plt.xlabel('Price in USD')
plt.ylabel('Number of Games')
plt.show() # Display the window

# Based on the graph, Majority of the games are priced between 0 - 70.
# Most famous games are priced around 20 - 60 dollars, while majority of the famous games are free which is around 50 games.


# Graph 2: Top 10 Genres of Games (Bar Plot)
# This bar chart shows the most popular game genre among the top steam games.
# Since one game can have many genres like Action and Indie, we split and "explode" them 
# So each genre gets its own row for counting.
genres_list = df_clean['genres'].str.split(', ').explode()
top_genres = genres_list.value_counts().head(10).reset_index()
top_genres.columns = ['Genre', 'Count']

plt.figure(figsize=(12, 6))
# Bar plot shows the ranking of the most common genres
sns.barplot(data=top_genres, x='Count', y='Genre', hue='Genre', palette='viridis')
# Title and label for the chart
plt.title('The Top 10 Most Common Genres')
plt.xlabel('Number Of Games')
plt.show()  # Display the window

# Based on the graph, Action and Indie games are the most common genre with 70 Games each. Followed by Adventure, RPG, Strategy and others.

# Graph 3: Correlation Heatmap 
# This is a heatmap that shows how different number metrics of the game relate to each other.
# Such as the price, positive and negative reviews, peak concurrent users, and estimated owners.
plt.figure(figsize=(10, 6))
# Select only numeric columns to see how they affect each other
corr_cols = ['price_usd', 'positive_reviews', 'negative_reviews', 'peak_ccu', 'estimated_owners_lower']
# .corr() calculates the relationship strength (closer to 1.0 = stronger link)
sns.heatmap(df_clean[corr_cols].corr(), annot=True, cmap='coolwarm', fmt=".2f")
# TItle for the chart
plt.title('Relationship Between Game Metrics (Correlation)')
plt.show() # Display the window

