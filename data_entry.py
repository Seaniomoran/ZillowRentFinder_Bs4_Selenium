from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class AutoDataEntry:
    def __init__(self, driver_path):
        ser = Service(driver_path)
        op = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(service=ser, options=op)
        self.driver.implicitly_wait(30)
        self.all_property_links = []
        self.all_prices = []
        self.all_addresses = []

    def zillow_get_links(self):

        zillow_url = "https://www.zillow.com/new-york-ny/rentals/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22New%20York%2C%20NY%22%2C%22mapBounds%22%3A%7B%22west%22%3A-74.72263143945312%2C%22east%22%3A-73.23673056054687%2C%22south%22%3A40.298413484751656%2C%22north%22%3A41.094908893698786%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A6181%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22min%22%3A0%2C%22max%22%3A872627%7D%2C%22mp%22%3A%7B%22min%22%3A0%2C%22max%22%3A3000%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%7D"

        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        accept_language = "en-US,en;q=0.9"
        headers = {
            "User-Agent": user_agent,
            "Accept-Language": accept_language,
        }
        response = requests.get(url=zillow_url, headers=headers)
        response.raise_for_status()
        zillow_page = response.text
        soup = BeautifulSoup(zillow_page, features="html.parser")

        all_link_elements = soup.select(".list-card-top a")
        # all_property_links = []
        for i in all_link_elements:
            href = i["href"]
            if "https" not in href:
                self.all_property_links.append(f"https://www.zillow.com{href}")
            else:
                self.all_property_links.append(href)

        all_price_elements = soup.select(".list-card-price")
        # all_prices = []
        for i in all_price_elements:
            price = i.text
            price = price.split("+")[0]
            self.all_prices.append(price)

        all_address_elements = soup.select(".list-card-addr")
        # all_addresses = []
        for i in all_address_elements:
            address = i.text
            address = address.split("| ")[1]
            self.all_addresses.append(address)

    def list_to_excel(self):
        form_link = "https://docs.google.com/forms/d/e/1FAIpQLScqqxLvhYiZvbtRXbP6ii8X_oQnBAV8NN4YtC6JSQID3clL7Q/viewform?usp=sf_link"
        self.driver.get(form_link)
        for i in range(len(self.all_property_links)):
            form_text = self.driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
            form_text.send_keys(f"{self.all_addresses[i]}{Keys.TAB}{self.all_prices[i]}{Keys.TAB}{self.all_property_links[i]}")
            submit = self.driver.find_element(By.CSS_SELECTOR, ".VkkpIf.QvWxOd")
            submit.click()
            new_response = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
            new_response.click()
