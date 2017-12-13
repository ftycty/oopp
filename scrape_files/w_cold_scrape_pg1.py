from urllib.request import urlopen as uReq
from urllib.request import Request
from bs4 import BeautifulSoup as soup
# -*- coding:utf-8 -*-

my_url = Request('http://www.watsons.com.sg/health/colds/flu/nasal/c/010102',headers={'User-Agent': 'Mozilla/5.0'})

uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html,'html.parser')
containers = page_soup.findAll('div',{'class':'productItemContainer'})

f = open('w_cold_scrape_pg1.csv','w', encoding="utf-8")

headers = 'name, price, offer, link, image\n'

f.write(headers)

for container in containers:
    pdt_container = container.findAll('div',{'class':'productInfoContainer'})

    pdt_name = container.findAll('p',{'class':'brandName'})[0].text + '|' + container.findAll('p',{'class':'productName'})[0].text

    pdt_price = container.findAll('p',{'class':'promoPrice'})[0].text.strip()

    pdt_offer = container.findAll('div',{'productPromotionTag'})[0].text.strip()

    if pdt_offer == 'PWP':
        pdt_offer = 'None'

    pdt_link = container.findAll('div',{'class':'productNameInfo'})[0].a['href']

    pdt_image = container.findAll('div',{'class':'productItemPhotoContainer'})[0].a.img['src']

    print('name:',pdt_name)
    print('price:', pdt_price)
    print('offer:', pdt_offer)
    print('link:',pdt_link)
    print('img:', pdt_image)
    print('________________')

    f.write(pdt_name.replace(',','|') + ',' + pdt_price + ',' + pdt_offer + ',' + pdt_link + ',' + pdt_image +'\n')

f.close()
