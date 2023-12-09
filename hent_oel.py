
import requests
import pandas as pd
import re
from bs4 import BeautifulSoup


import urllib.request    
urllib.request.urlretrieve("https://untappd.com/user/MathiasB91/beers", "untappd.html")


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

# ABV
abv_elements = soup.find_all(class_='abv')
abv_values = [float(re.search(r'\d+\.\d+', element.get_text(strip=True)).group()) if re.search(r'\d+\.\d+', element.get_text(strip=True)) else 0 for element in abv_elements]

# IBU
ibu_elements = soup.find_all(class_='ibu')
ibu_values = [float(re.search(r'\d+', element.get_text(strip=True)).group()) if re.search(r'\d+', element.get_text(strip=True)) else 0 for element in ibu_elements]


# Create a DataFrame with the names and breweries
df = pd.DataFrame({'Øl': names, 'Bryggeri': breweries, 'ABV': abv_values, 'IBU': ibu_values})

# Display the DataFrame
print(df)
