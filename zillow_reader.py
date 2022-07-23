from bs4 import BeautifulSoup
import requests

# def send_email(email_dict):
#     with smtplib.SMTP(EMAIL_PROVIDER_SMTP_ADDRESS) as connection:
#         connection.starttls()  # makes connection secure
#         connection.login(user=my_email, password=my_password)
#         letter_text = ""
#         for i in email_dict:
#             letter_text += f"{i} costs {email_dict[i]['cost']} is down {email_dict[i]['percent']} from {email_dict[i]['orig_cost']}\n{email_dict[i]['website']}\n\n"
#
#         connection.sendmail(from_addr=my_email, to_addrs=my_email,
#                             msg=f"Subject: Amazon Sale!\n\nThese products have decreased in price!:\n\n{letter_text}")






user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
accept_language = "en-US,en;q=0.9"
headers = {
    "User-Agent": user_agent,
    "Accept-Language": accept_language,
}

df = pd.read_csv("amazon_item&url.csv", index_col=False)
item_dict = df.set_index("item").T.to_dict()
print(item_dict)

email_dict = {}
item_url = ""
for item in item_dict:
    item_url = item_dict[item]["website"]
    item_orig_price = item_dict[item]["orig_price"]

    response = requests.get(url=item_url, headers=headers)
    response.raise_for_status()
    amazon_web_page = response.text
    soup = BeautifulSoup(amazon_web_page, features="lxml")
    price = [price.getText().replace(",", "") for price in soup.find(name="span", class_="a-price-whole")][0]
    fraction = [fraction.getText() for fraction in soup.find(name="span", class_="a-price-fraction")][0]
    price = float(f"{price}.{fraction}")
    percent_decrease = 100 - price/item_orig_price * 100
    print(percent_decrease)

    if percent_decrease >= 5:
        email_dict[item] = {
            'cost': price,
            'website': item_url,
            'percent': percent_decrease,
            'orig_cost': item_orig_price,
        }
    print(email_dict)

if email_dict != {}:
    send_email(email_dict)