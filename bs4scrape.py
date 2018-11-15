import math

import bs4
import requests


class BsScrape:

    def __init__(self, url):
        self.url = url
        self.res = requests.get(self.url)
        self.car_list_data = bs4.BeautifulSoup(self.res.text, "html.parser")
        self.base_url = 'https://www.carsales.com.au'
        self.no_pages_searched = 0

    def calculate_no_pages(self):
        # Gets the string that states how many cars are for sale.
        total_cars_for_sale = self.car_list_data.select('div h1')
        # Pulls the int from the string data.
        # Removes the comma if the number of cars is > 1000
        int_cars_for_sale = int(total_cars_for_sale[0].getText().split()[0].replace(',', ''))
        # Divides by 12 to determine number of pages to scrape.
        # Only 12 cars per page are shown.
        self.no_pages_searched = math.ceil(int_cars_for_sale / 12)
        return self.no_pages_searched

    def next_page(self):
        next_page_element = self.car_list_data.select('li.next.tippable a')
        additional_string = str(next_page_element[0].get('href'))
        new_url = self.base_url + additional_string
        return new_url



