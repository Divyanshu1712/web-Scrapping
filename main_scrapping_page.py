import requests
from bs4 import BeautifulSoup
import pandas as pd
from openpyxl.workbook import Workbook
import json

# Step 1: Target e-commerce URL
url = "https://fashion-tac.vercel.app/"  # Replace with the actual URL of the iPhone page

# Step 2: Fetch page content
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    content = response.text
else:
    print(f"Failed to fetch the URL: {response.status_code}")
    exit()

# Step 3: Parse the content
soup = BeautifulSoup(content, "html.parser")
# print(soup.prettify())

# Step 4: Extract data
products = []  # List to store product details

# Modify selectors based on the website structure

div_data = soup.find_all("div", class_="product")

for product in div_data:
    name_of_product = product.find('h3', class_ ="product__name").text.strip() if product.find('h3',class_="product__name") else "N/A"
    price_of_product = product.find('p', class_ ="product__price").text.strip() if product.find('p',class_="product__price") else "N/A"
    # print(f"Name: {name_of_product} and price : {price_of_product}\n")
    products.append({
        "Product": name_of_product,
        "Price": price_of_product 
    })

json_setup = json.dumps(products, indent=4)

with open("mine/data.json",'w') as fp:
    fp.write(json_setup)


# Step 5: Convert data to DataFrame
df = pd.DataFrame(products)

# Step 6: Save to Excel
output_file = "mine/ProductList.xlsx"
df.to_excel(output_file, index=False, engine="openpyxl")

print(f"Data saved to {output_file}")
