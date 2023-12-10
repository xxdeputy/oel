# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 19:59:11 2023

@author: Mathias
"""

import requests
import pandas as pd
import re
from bs4 import BeautifulSoup
from datetime import datetime


import urllib.request    
urllib.request.urlretrieve("https://untappd.com/user/MathiasB91/beers", "untappd.html")


# Lokal fil
html_file_path = "C:/Users/Mathias/Documents/Dokumenter/113 Brewing/untappd.html"


# Your input string containing "alt=NAME" instances
#html_file_path = "C:/Users/Mathias/untappd.html"



# Read the HTML content from the file
with open(html_file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Beer
name_elements = soup.select('.name:not(.sidebar .name)')
names = [element.get_text(strip=True) for element in name_elements]

# Brewery
brewery_elements = soup.find_all(class_='brewery')
breweries = [element.get_text(strip=True) for element in brewery_elements]

# Stil
style_elements = soup.find_all(class_='style')
styles = [element.get_text(strip=True) for element in style_elements]
split_styles = [tuple(part.strip() for part in style.split("-")) for style in styles]

Type_list = []
Undertype_list = []

# Split each element of 'styles' using "-" delimiter and assign to separate variables
for style in styles:
    parts = [part.strip() for part in style.split(" - ")]
    Type = parts[0]
    Undertype = parts[1] if len(parts) > 1 else ''  # Check if there is a second part
    Type_list.append(Type)
    Undertype_list.append(Undertype)

# ABV
abv_elements = soup.find_all(class_='abv')
abv_values = []
for element in abv_elements:
    text = element.get_text(strip=True)
    try:
        abv_value = float(re.search(r'\d+(\.\d+)?', text).group())
    except (ValueError, AttributeError):
        print(f"Could not convert '{text}' to float.")
        abv_value = 0
    abv_values.append(abv_value)

# IBU
ibu_elements = soup.find_all(class_='ibu')
ibu_values = [float(re.search(r'\d+', element.get_text(strip=True)).group()) if re.search(r'\d+', element.get_text(strip=True)) else 0 for element in ibu_elements]


#Rating, både min og global
# Find all elements with class 'ratings'
rating_elements = soup.find_all(class_='ratings')
ratings = [element.get_text(strip=True) for element in rating_elements]
min_ratings2 = [rating[:21] for rating in ratings]
min_ratings1 = [re.sub(r'[^0-9.-]', '', rating) for rating in min_ratings2]
My_Rating = [float(rating) if rating else 0 for rating in min_ratings1]

global_rating2 = [rating[29:54] for rating in ratings]
# Use regular expressions to keep only numeric characters
global_rating1 = [re.sub(r'[^0-9.-]', '', rating) for rating in global_rating2]
# Convert to numeric values
Global_Rating = [float(rating) if rating else 0 for rating in global_rating1]


# Date
# Find all elements with class 'date'
date_elements = soup.find_all(class_='date')
# Extract the date values using BeautifulSoup
dates = [element.get_text(strip=True) for element in date_elements]
# Keep only elements containing 'Recent' in the list
Dato = [''.join(char for char in date if char.isdigit() or char == '/') for date in dates if 'Recent' in date]
Date = [datetime.strptime(date, '%m/%d/%y').date() for date in Dato]



# Create a DataFrame with the names and breweries
df = pd.DataFrame({'Beer': names, 'Brewery': breweries, 'Type': Type_list, 'Subtype': Undertype_list, 'ABV': abv_values, 'IBU': ibu_values, 'My_Rating': My_Rating, 'Global_Rating': Global_Rating, 'Date_time':Date})

# Display the DataFrame
print(df)
