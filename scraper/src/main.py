import requests
import logging
from bs4 import BeautifulSoup
from models import AdvertModel

# URL of the webpage you want to scrape
URL = "https://flatfy.ua/uk/search?geo_id=24&section_id=2"  # Replace with the URL of the webpage you want to scrape


def get_advert_page(advert):
    logging.info(f"Getting page for {advert.title}")
    response = requests.get(advert.url)

    return response.text


def main():
    # Send an HTTP GET request to the URL
    response = requests.get(URL)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        with open("temp/sample.html", "w+", encoding="utf-8") as f:
            f.write(response.text)
        # Parse the HTML content of the webpage using BeautifulSoup
        main_page = BeautifulSoup(response.text, "html.parser")

        # Find the first <div> element with class "realty-preview__base"
        card_divs = main_page.find_all("div", class_="realty-preview__base")

        if card_divs:
            # Loop through and print the contents of each matching div
            for div in card_divs:
                title = div.find(class_="realty-preview-sub-title").text
                price = div.find(class_="realty-preview-price realty-preview-price--main").text
                address = div.find(class_='realty-preview-title').text
                amount_rooms = div.find(class_='realty-preview-info').text
                description = div.find(class_='realty-preview-description__text').text
                advert_url = 'https://flatfy.ua' + div.find('a')['href']

                advert = AdvertModel(url=advert_url, title=title, price=price, address=address, amount_rooms=amount_rooms, description=description)

                advert_page = BeautifulSoup(get_advert_page(advert), "html.parser")
                image_divs = advert_page.find_all("div", class_="image-carousel-slide")

                for image_div in image_divs:
                    advert.image_urls.append(image_div.find("img").get("src"))

        else:
            print("No divs with data-cy='l-card' found on the webpage.")
    else:
        print(f"Failed to retrieve the webpage (Status Code: {response.status_code})")


if __name__ == "__main__":
    main()
