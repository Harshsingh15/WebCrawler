import requests
from bs4 import BeautifulSoup
import csv

products = []
urls = ["https://scrapeme.live/shop/"]

while len(urls) != 0:
    current_url = urls.pop()

    response = requests.get(current_url)
    soup = BeautifulSoup(response.content, "html.parser")

    link_elements = soup.select("a[href]")

    for link_element in link_elements:
        url = link_element["href"]
        if "https://scrapeme.live/shop" in url:
            urls.append(url)

    product = {}
    product["url"] = current_url

    image_element = soup.select_one(".wp-post-image")
    product["image"] = image_element["src"] if image_element else None

    title_element = soup.select_one(".product_title")
    product["name"] = title_element.text if title_element else None

    price_element = soup.select_one(".price")
    product["price"] = price_element.text if price_element else None

    products.append(product)

with open('products.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["URL", "Image", "Name", "Price"])

    for product in products:
        writer.writerow([product["url"], product["image"], product["name"], product["price"]])
