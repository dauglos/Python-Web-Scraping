import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import math

#Creating a requisition to acess the data, Headers will be used to ensure that permission problems won't come by
link = 'https://www.kabum.com.br/hardware/placa-de-video-vga'
headerPermission = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.84'}
siteReq= requests.get(link, headers=headerPermission)

# We create a BeautifulSoup object in order to properly parse the Html info in the website
soupObj= BeautifulSoup(siteReq.content,'html.parser')

# We need to know how many pages we will have to go through, a quick calculation, total number of items divided by items by pages will do the trick
# But we need the number on its own, só we will strip it and remove the blank space the html provides.

quantityItems= soupObj.find('div', id='listingCount').text.strip()
indexBlank = quantityItems.find(' ')
quantityFinal=quantityItems[:indexBlank]
lastPage = math.ceil(int(quantityFinal)/ 20)

#Lets create a dicionary to append the info we want about the vgas.
prodDic = {'brand':[], 'price':[]}

#Lets use a for to go through our pages, format string will do the trick for us in order to go on page by page.
# notice we need to  add+1 to our lastPage var because Python is exclusive.

for i in range(1, lastPage+1):
    url_page = f'https://www.kabum.com.br/hardware/placa-de-video-vga?page_number={i}&page_size=20&facet_filters=&sort=most_searched'
    siteReq = requests.get(url_page, headers=headerPermission)
    soupObj = BeautifulSoup(siteReq.content, 'html.parser')
    prods = soupObj.find_all('div', class_=re.compile('productCard'))

#Now we do a for in order to cycle through the info we need in every page
    for prod in prods:
        brand = prod.find('span', class_=re.compile('nameCard')).get_text().strip()
        price = prod.find('span', class_=re.compile('priceCard')).get_text().strip()

        print(brand, price)
# and then we append the info to the dictionary we created up there.
        prodDic['brand'].append(brand)
        prodDic['price'].append(price)
#We print our Scraped info
    print(url_page)

#And now we create the CSV file
df = pd.DataFrame(prodDic)
df.to_csv('C:/Users/PC/Desktop/cadeiras.csv',encoding='utf-8', sep=';')
