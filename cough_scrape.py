from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
# -*- coding:utf-8 -*-
my_url = 'https://www.guardian.com.sg/health/pl/Cough%2C%20Cold%20%26%20Allergy'

uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html,'html.parser')
containers = page_soup.findAll('div',{'class':'listing-item'})

f = open('cough_pg1.csv','w', encoding="utf-8")

headers = 'name, price, offer, link, image\n'

f.write(headers)

for container in containers:
    pdt_name = container.div.a['title']

    price_container = container.findAll('div',{'class':'listing-item-price'})
    pdt_price = price_container[0].text.strip()

    offer_container = container.findAll('div',{'product-offer'})
    pdt_offer = offer_container[0].text.strip()

    pdt_link = container.div.a['href']

    pdt_image = container.div.a.img['src']

    print('name:',pdt_name)
    print('price:', pdt_price)
    print('offer:', pdt_offer)
    print('link:',pdt_link)
    print('img:', pdt_image)
    print('________________')

    f.write(pdt_name.replace(',','|') + ',' + pdt_price + ',' + pdt_offer + ',' + pdt_link + ',' + pdt_image +'\n')

f.close()
