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


# Prepare Data Sets for each Graph
# Storing Neccessary Data as a variable to use

# Graph 2 Bar Plot Tools
# Since one game can have many genres like Action and Indie, we split and "explode" them 
# So each genre gets its own row for counting.
genres_list = df_clean['genres'].str.split(', ').explode()
top_genres = genres_list.value_counts().head(10).reset_index()
top_genres.columns = ['Genre', 'Count']

# Graph 3 HeatMap Tool
# Select only numeric columns to see how they affect each other
corr_cols = ['price_usd', 'positive_reviews', 'negative_reviews', 'peak_ccu', 'estimated_owners_lower']

# Graph 4 Line Plot Tool
# Group the data by their release year and count how many games were released that year
release_trend = df_clean.groupby('release_year').size().reset_index(name='count')
# ------------------------------------------------------------------------------------------------------------------------
# Graph Visualizations Section

# Graphs are Put into functions because they are put into slides for easier navigation.
# Each function takes an "ax" argument which is the area where the graph will be drawn, this allows us to reuse the same function for both individual slides and the final dashboard slide.
# Each graph is drawn depending on where the current slide is, it calls the function to draw the graph based on the given data.
# So all data is prepared in those functions.

# Graph 1: Distribution of Game Prices (Histogram Plot)
# This Histplot shows how much these games costs on steam and how many games fall into each price range.
# We filtered out the games that are under 100$ to avoid long tails on the chart, which can make it harder to see the distribution.

def plot_1_prices(ax):
    # Filter to games under $100 to avoid long "tails" on the chart
    sns.histplot(df_clean[df_clean['price_usd'] < 100]['price_usd'], bins=30, kde=True, color='skyblue', ax=ax)
    # Title and Labels for the chart
    ax.set_title('Graph 1: Price Distribution (Use Arrow Keys to Move)')
    ax.set_xlabel('Price in USD')

# Based on the graph, Majority of the games are priced between 0 - 70.
# Most famous games are priced around 20 - 60 dollars, while majority of the famous games are free which is around 50 games.


# Graph 2: Top 10 Genres of Games (Bar Plot)
# This bar chart shows the most popular game genre among the top steam games.
# Since one game can have many genres like Action and Indie, we split and "explode" them 
# So each genre gets its own row for counting.

def plot_2_genres(ax):
    sns.barplot(data=top_genres, x='Count', y='Genre', hue='Genre', palette='viridis', ax=ax)
    ax.set_title('Graph 2: Top 10 Common Genres')
    ax.set_xlabel('Number of Games')

# Based on the graph, Action and Indie games are the most common genre with 70 Games each. Followed by Adventure, RPG, Strategy and others.

# Graph 3: Correlation Heatmap (HeatMap)
# This is a heatmap that shows how different number metrics of the game relate to each other.
# Such as the price, positive and negative reviews, peak concurrent users, and estimated owners.

def plot_3_heatmap(ax):
    # .corr() calculates the relationship strength (closer to 1.0 = stronger link)
    sns.heatmap(df_clean[corr_cols].corr(), annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
    ax.set_title('Graph 3: Correlation Heatmap')


# Graph 4: Release Trends Over Time (Line Plot)
# This line plots show when the most popular games were released over the years and how many games were released each year
# Seeing the release trends over time

def plot_4_trends(ax):
    sns.lineplot(data=release_trend, x='release_year', y='count', marker='o', color='red', ax=ax)
    ax.set_title('Graph 4: Games Released per Year')
    ax.set_xlabel('Release Year')


# Graph 5 : Quality Vs Price (Scatter Plot)
# This scatter plot shows the price of the game on the x axis and the metacritic score on the y axis.
# Metacritic score is a common way to check the quality of a game, on a scale of 100 , 100 is the best score.
def plot_5_quality(ax):
    # We drop rows without a Metacritic score for this specific plot
    quality_df = df_clean.dropna(subset=['metacritic_score'])
    sns.scatterplot(data=quality_df, x='price_usd', y='metacritic_score', alpha=0.6, ax=ax)
    sns.regplot(data=quality_df, x='price_usd', y='metacritic_score', scatter=False, color='black', ax=ax)
    ax.set_title('Graph 5: Quality Vs Price')
    ax.set_xlabel("Price (USD)")
    ax.set_ylabel("Metacritic Score")

# Graph 6 : Platform Accessibility (Pie Chart)
# This pie chart shows how many games support mac/linux vs windows.
def plot_6_platform(ax):
    # Calculate how many games support Mac/Linux vs only Windows
    mac_linux = len(df_clean[(df_clean['platforms_mac'] == True) | (df_clean['platforms_linux'] == True)])
    windows_only = len(df_clean) - mac_linux
    
    labels = ['Cross-Platform (Mac/Linux)', 'Windows Only']
    sizes = [mac_linux, windows_only]
    colors = ['#66b3ff', '#ff9999']
    
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors, explode=(0.1, 0))
    ax.set_title('Graph 6: Platform Accessibility')


# ---------------------------------------------------------------------------------------------------------------------------

# Dashboard Slide, A Combination of all the graphs in one slide.

def dashboard(fig):
    # This function is special because it clears the whole figure to create subplots
    fig.clf() 
    axes = fig.subplots(3, 2)
    
    # Fill the dashboard slots
    # Histogram Plot of Prices
    sns.histplot(df_clean[df_clean['price_usd'] < 100]['price_usd'], ax=axes[0,0], color='skyblue')
    axes[0,0].set_title('Prices')
    
    # Bar Plot Of Genres
    sns.barplot(data=top_genres, x='Count', y='Genre', ax=axes[0,1], palette='viridis')
    axes[0,1].set_title('Genres')
    
    # Heatmap of Correlations
    sns.heatmap(df_clean[corr_cols].corr(), annot=True, ax=axes[1,0], cmap='coolwarm', cbar=False)
    axes[1,0].set_title('Correlation')
    
    # Line Plot of Release Trends
    sns.lineplot(data=release_trend, x='release_year', y='count', ax=axes[1,1], color='red')
    axes[1,1].set_title('Trends')

    # Scatter Plot of Quality vs Price
    plot_5_quality(axes[2, 0])
    axes[2, 0].set_title('Quality vs. Price')
    
    # Pie Chart of Platform Accesibility
    plot_6_platform(axes[2, 1])
    plt.axes[2,1].set_title('Platform Support')
    
    # Dashboard Tools
    fig.suptitle("Final Slide: Summary Dashboard", fontsize=16)
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])

# ---------------------------------------------------------------------------------------------------------------------------
# Slide Manager and Nav Logic

# List of slides
slides = [plot_1_prices, plot_2_genres, plot_3_heatmap, plot_4_trends, plot_5_quality, plot_6_platform, dashboard]
current_slide = 0

# Function to handle key Presses
def on_key(event):
    global current_slide
    # RIght Key press
    if event.key == 'right':
        current_slide = (current_slide + 1) % len(slides)
    # Left Key Press
    elif event.key == 'left':
        current_slide = (current_slide - 1) % len(slides)
    else:
        return # Ignore other keys
    
    fig.clf()
    # Redraw logic
    if slides[current_slide] == dashboard:
        fig.set_size_inches(16, 12)
        dashboard(fig)
    else:
        fig.set_size_inches(10, 6)
        new_ax = fig.add_subplot(111)
        slides[current_slide](new_ax)
    
    # Draw the Updated Graph
    plt.draw()

# Initial display
fig, ax = plt.subplots(figsize=(10, 6))
slides[current_slide](ax)

# Connect the key press function 
fig.canvas.mpl_connect('key_press_event', on_key)

print("Press Left and Right Arrow Keys to Navigate Through the Graphs")
plt.show()