# Importing Essential Libraries
# Such as Panda for Data Manipulation
# MatplotLib for Plotting Graphs
# and Seaborn for Statistical Data Visualization

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Import Data from a CSV File
# Data is From Kaggle Dataset of Top Steam Games
# https://www.kaggle.com/datasets/patelris/steam-top-1495-games-dataset

# Df is Data Frame and it uses the panda read function to read the csv file and storing it.
df = pd.read_csv('steam_top_games_2026.csv')
