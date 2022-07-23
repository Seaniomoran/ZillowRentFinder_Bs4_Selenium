from data_entry import AutoDataEntry
import os

#your driver path
DRIVER_PATH = os.getenv('DRIVER_PATH')  #your driver path

#using bot to log in
bot = AutoDataEntry(driver_path=DRIVER_PATH)
bot.zillow_get_links()
bot.list_to_excel()

