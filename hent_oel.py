# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 19:59:11 2023

@author: Mathias
"""

import requests
import pandas as pd
import re
from bs4 import BeautifulSoup


import urllib.request    
urllib.request.urlretrieve("https://untappd.com/user/MathiasB91/beers", "untappd.html")


# Lokal fil
# html_file_path = "C:/Users/Mathias/Documents/Dokumenter/113 Brewing/untappd.html"


# Your input string containing "alt=NAME" instances
html_file_path = "C:/Users/Mathias/untappd.html"



# Read the HTML content from the file
with open(html_file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Ølnavn
name_elements = soup.select('.name:not(.sidebar .name)')
names = [element.get_text(strip=True) for element in name_elements]

# Bryggeri
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

# Date
date_elements = soup.find_all(class_='date-time')
date_values = [element.get_text(strip=True) for element in date_elements]
unique_date_values = list(set(date_values))

# Create a DataFrame with the names and breweries
df = pd.DataFrame({'Øl': names, 'Bryggeri': breweries, 'Type': Type_list, 'Undertype': Undertype_list, 'ABV': abv_values, 'IBU': ibu_values})

# Display the DataFrame
print(df)
