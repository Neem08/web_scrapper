import requests
from lxml import html
from pymongo import MongoClient

# Define the MongoDB connection
client = MongoClient('mongodb+srv://neemisha:paul123@cluster0.se6opob.mongodb.net/')  # Change the URL to your MongoDB server

# Create or access a database
db = client['furniture']  # Change 'mydatabase' to your preferred database name

# Create or access a collection within the database
collection = db['my_fur']  # Change 'mycollection' to your preferred collection name

# Define the URL of the website you want to scrape
url = 'https://www.at-home.co.in/collections/1-seater-sofa'


response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page using lxml
    tree = html.fromstring(response.content)

    # Use CSS selectors to extract the product elements
    product_elements = tree.cssselect('.boost-pfs-filter-product-item')

    # Iterate through the extracted product elements and extract name and price
    for product_element in product_elements:
        # Use CSS selectors to extract the name
        name_element = product_element.cssselect('.boost-pfs-filter-product-item-title')
        name = name_element[0].text.strip() if name_element else ""

        # Use CSS selectors to extract the price
        price_element = product_element.cssselect('.boost-pfs-filter-product-item-sale-price span')
        price = price_element[1].text.strip() if len(price_element) > 1 else ""

        # Create a document to insert into the collection
        document = {
            'name': name,
            'price': price,
        }
        # Insert the document into the collection
        collection.insert_one(document)
        print(document)

    print('Scraping and data insertion completed.')
else:
    print('Failed to retrieve the web page.')

# Close the MongoDB connection
client.close()



