from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url = 'https://www.guardian.com.sg/health/pl/Cough%2C%20Cold%20%26%20Allergy'

uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html,'html.parser')
containers = page_soup.findAll('div',{'class':'listing-item'})

f = open('cough_cold_allergy.csv','w')

headers = 'name, price, offer\n'

f.write(headers)

for container in containers:
    pdt_name = container.div.a['title']

    price_container = container.findAll('div',{'class':'listing-item-price'})
    pdt_price = price_container[0].text.strip()

    offer_container = container.findAll('div',{'product-offer'})
    pdt_offer = offer_container[0].text.strip()

    print('name:',pdt_name)
    print('price:', pdt_price)
    print('offer:', pdt_offer)

    f.write(pdt_name + ',' + pdt_price + ',' + pdt_offer + '\n')

f.close()
