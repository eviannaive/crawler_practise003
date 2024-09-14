from operator import index

import requests
from bs4 import BeautifulSoup
import pandas as pd

url= "https://chart.capital.com.tw/Chart/TWII/TAIEX11.aspx"

response = requests.get(url)

get_els = lambda el : el.has_attr("id")
filename = "stock_data.xlsx"
data_list = []

if response.status_code == requests.codes.ok:
    # soup = BeautifulSoup(response.text, "html.parser")
    soup = BeautifulSoup(response.text, "lxml") #另一種更快速的解析，但要安裝
    # print(soup.prettify())
    tr_with_id = soup.find_all("tr",id=True)

    # for d in tr_with_id:
    #     tds = d.find_all("td")
    #     tds_text = list(map(lambda td : td.text, tds))
    #     data_list.append(tds_text)
    #     print(f"寫入{tds_text}...")

    for d in tr_with_id:
        tds = d.find_all("td")
        date, value, price = [cell.text for cell in tds]
        data_list.append([date,value,price])
        print(f"寫入{date},{value},{price}...")


    print("export excel...")
    empty_file = pd.DataFrame(data_list,columns=["日期", "買賣超金額", "台指期"])
    empty_file.to_excel(filename, index=False, engine='openpyxl')
    print("export success!")
