import pandas as pd
import requests
from bs4 import BeautifulSoup

res = requests.get(
    "https://www.valueresearchonline.com/funds/16854/franklin-india-ultra-short-bond-fund-super-institutional-plan-direct-plan/")

soup = BeautifulSoup(res.text, "html.parser")

# table = soup.find("table", {"id": "trailing-returns-table"})
table = soup.find("table", {"id": "trailing-returns-table"})
columns = [i.get_text(strip=True) for i in table.find_all("th")]
data = []

for tr in table.find("tbody").find_all("tr"):
    data.append([td.get_text(strip=True) for td in tr.find_all("td")])

df = pd.DataFrame(data, columns=columns)

df.to_excel("data.xlsx", index=False)
