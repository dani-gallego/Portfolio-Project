import httpx
from bs4 import BeautifulSoup
import csv
import datetime
import os


URL = 'https://www.ebay.ph/b/Consumer-Electronics/293/bn_1865552'

headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
}


# Global variable - Empty list
product_data = []


def main():
    get_products_url()

    save_to_csv(product_data)
    append_new_data(product_data)
    print(f'Saved {len(product_data)} products to Ebay: Consumer Electronics')

# Getting the URL using httpx and find products using BeautifulSoup
def get_products_url():
    response = httpx.get(URL)
    response_html = response.text
 
    # Pass html parser
    soup = BeautifulSoup(response_html, 'html.parser')


    # Find all products
    products = soup.find_all('div', class_='brwrvr__item-card__body')


    # Error handling
    for product in products :
        title_name, price = extract_product_data(product)
        if title_name and price:
            product_data.append((title_name,price))

# Extracting the product data
def extract_product_data(product):

    # first_product.find('span', class_='bsig__title').text
    # first_product.find('span', class_='textual-display bsig__price bsig__price--displayprice').text

    try:
        title_name = product.find('span', class_='bsig__title').text
        if title_name.startswith("New Listing"):
            title_name = title_name[11:].strip()  # Remove the first 11 characters
        
        price = product.find('span', class_='textual-display bsig__price bsig__price--displayprice').text
        
        print(f'Product Name: {title_name} Price: {price}')

        return title_name, price
    
    except Exception as e:
        print(e)
        return None, None

# Creating a new CSV
def save_to_csv(products):
    date = datetime.date.today()
    header = ['Date', 'Product Name', 'Price']

    # Writing the data to CSV file
    with open('EbayConsumerElectronics.csv', 'w', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)

        for product in products:
            writer.writerow([date, *product])

# Appending a new data from CSV
def append_new_data(products):
    date = datetime.date.today()

    # Load existing data from the CSV into a set
    existing_data = set()
    if os.path.exists('EbayConsumerElectronics.csv'):
        with open('EbayConsumerElectronics.csv', 'r', encoding='UTF8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip the header
            for row in reader:
                if len(row) >= 3:  # Ensure the row has enough columns
                    existing_data.add((row[1], row[2]))  # Add (Product Name, Price) tuple

    # Appending only new, unique data
    with open('EbayConsumerElectronics.csv', 'a', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        for product in products:
            if product not in existing_data:  # Only append if the product is not a duplicate
                writer.writerow([date, *product])

if __name__ == '__main__':
    main()