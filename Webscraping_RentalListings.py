
# coding: utf-8

# In[ ]:

# APARTMENT LISTINGS FROM CRAIGSLIST

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import csv # fab's code
from datetime import datetime
import os
import time
from random import randint

x = datetime.today()
filename = 'Craiglist_Rental_'+ x.strftime('%Y-%m-%d_%H%M') +'.csv'
outputfolder = r"C:\Users\Fabienne\Documents\Webscraping_RentalListings"

# Latest four pages of listings (480 total).
page1 = "https://toronto.craigslist.ca/search/tor/apa"
page2 = "https://toronto.craigslist.ca/search/tor/apa?s=120"
page3 = "https://toronto.craigslist.ca/search/tor/apa?s=240"
page4 = "https://toronto.craigslist.ca/search/tor/apa?s=360"

all_pages = [page1,page2,page3,page4]

with open(os.path.join(outputfolder, filename), 'w', newline='', encoding='utf-8') as file:

    # Create headers
    file.write('listing_name,post_id,address,address2,rent,bedrooms,datetime_posted,size,availability,description,attributes,lat,lon,html,\n')
    
    for page in all_pages:
        page_html = urlopen(page).read()
        page_soup = soup(page_html, "html.parser")
        containers = page_soup.findAll("li", {"class":"result-row"})

        for container in containers:
            container = container.p

            listing_name = container.a.text

            address = container.find("span", {"class":"result-hood"})
            if address == None:
                address = 'NA'
            else:
                address = address.text.strip()

            rent = container.find("span", {"class":"result-price"}).text

            datetime_posted = container.time["datetime"]

            html = container.a["href"]
            item_page = urlopen(html).read()
            item_soup = soup(item_page, "html.parser")

            top_attr = item_soup.findAll("span", {"class":"shared-line-bubble"})
            if len(top_attr) == 3:
                bedrooms = top_attr[0].text
                size = top_attr[1].text
                availability = top_attr[2]["data-date"]
            if len(top_attr) == 2:
                if len(top_attr[0].text) <8:
                    size = top_attr[0].text
                    bedrooms = 'NA'
                else:
                    bedrooms = top_attr[0].text
                    size = 'NA'
                availability = top_attr[1]["data-date"]

            address2 = item_soup.find("div",{"class":"mapaddress"})
            if address2 == None:
                address2 = 'NA'
            else:
                address2 = address2.text.strip()

            description_container = item_soup.find("section", {"id":"postingbody"})
            description = description_container.contents[2].strip()

            post_id = item_soup.find("div", {"class":"postinginfos"})
            post_id = post_id.p.text

            attributes = item_soup.findAll("p", {"class":"attrgroup"})[1].findAll("span")    
            attribute_list = []
            for attr in attributes:
                attr = attr.text
                attribute_list.append(attr)

            latlon_container = item_soup.find("div", {"id":"map"})
            if latlon_container == None:
                lat = 'N/A'
                lon = 'N/A'
            else:
                lat = latlon_container['data-latitude']
                lon = latlon_container['data-longitude']

            item_row = [[listing_name]+[post_id]+[address]+[address2]+[rent]+[bedrooms]+[datetime_posted]+[size]+[availability]+[description]+[attribute_list]+[lat]+[lon]+[html]]
            print(item_row)
            
            writer = csv.writer(file, delimiter = ",")
            writer.writerows(item_row)
            time.sleep(randint(30,120))
    print('Finished!')

