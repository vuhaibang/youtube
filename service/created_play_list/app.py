from bs4 import BeautifulSoup
import requests


# form_data={'Email': 'vuhaibangtk@gmail.com', 'Passwd': 'gE+X5TW`"5OnU10m'}
form_data={'Email': 'vuhaibang1994@gmail.com', 'Passwd': 'bang331511'}

post = "https://accounts.google.com/signin/challenge/sl/password"

s = requests.Session()
soup = BeautifulSoup(s.get("https://mail.google.com").text)
for inp in soup.select("#gaia_loginform input[name]"):
    if inp["name"] not in form_data:
        form_data[inp["name"]] = inp["value"]
s.post(post, form_data)