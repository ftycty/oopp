from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
# -*- coding:utf-8 -*-
my_url = 'https://www.guardian.com.sg/health/pl/Cough%2C%20Cold%20%26%20Allergy'

uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html,'html.parser')
containers = page_soup.findAll('div',{'class':'listing-item'})

f = open('g_cough_pg1.csv','w', encoding="utf-8")

headers = 'name, price, offer, link, image, message\n'

f.write(headers)

for container in containers:
    pdt_name = container.div.a['title']

    price_container = container.findAll('div',{'class':'listing-item-price'})
    pdt_price = price_container[0].text.strip()
    if '\n' in pdt_price:
        new = pdt_price.find('\n')
        pdt_price = pdt_price[:new]

    offer_container = container.findAll('div',{'product-offer'})
    pdt_offer = offer_container[0].text.strip()
    if pdt_offer == '':
        pdt_offer = 'No promotion available'

    pdt_link = container.div.a['href']

    pdt_image = container.div.a.img['src']

    try:
        pdt_msg = container.p.text.strip()
    except:
        pdt_msg = 'In Stock'
    # print('name:',pdt_name)
    # print('price:', pdt_price)
    # print('offer:', pdt_offer)
    # print('link:',pdt_link)
    # print('img:', pdt_image)
    # print('message:',pdt_msg)
    # print('________________')

    f.write(pdt_name.replace(',','|').replace('\n',' ') + ',' + pdt_price + ',' + pdt_offer + ',' + pdt_link + ',' + pdt_image + ',' + pdt_msg + '\n')

f.close()
