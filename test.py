import modules.mm_reality as mm
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

p = mm.GetScraped()

# i = 1
# url = 'https://www.mmreality.cz/nemovitosti/hledani/?&filter%5BfCategory%5D%5B%5D=10&filter%5BfEstateType' \
#                   '%5D=11&filter%5BfDisposition%5D%5B%5D=200&filter%5BfDisposition%5D%5B1%5D=55&filter%5BfDisposition' \
#                   '%5D%5B2%5D=201&filter%5BfDisposition%5D%5B3%5D=56&filter%5BfDisposition%5D%5B4%5D=202&filter%5Bf' \
#                   'Disposition%5D%5B5%5D=57&filter%5BfRegion%5D=116&filter%5BfDistrict%5D%5B%5D=3702&page=' + str(i)
#
# driver = webdriver.Chrome()
# driver.get(url)
# soup = BeautifulSoup(driver.page_source, "html.parser")
# driver.quit()
#
#
# offers_list = soup.select('.offersList')
# for offer in offers_list.select('.offerItem.'):
#     title = offer.find('a')['title']
#     split_title = title.split(',')
#     size = split_title[1]
#     loc = split_title[-1]
#     price = offer.select('strong.price')[0].text
#     link = 'https://www.mmreality.cz' + offer.select('a')[0]['href']
#     id = offer.select('a')[0]['href'][:-1].split('/')[-1]
#
#
# print(type(soup))


