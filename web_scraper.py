import csv
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import datetime

# bezrealitky sreality reality


class Scraper:
    def __init__(self):
        pass

    def scrape_page(self, page):
        
        page.import_from_csv()
        
        # pocet novych nabidek
        self.cnt_new = 0

        # BEZREALITKY
        if page.page_name == 'bezrealitky':
            for i in range(1, 11):
                url = 'https://www.bezrealitky.cz/vypis/nabidka-prodej/byt/jihomoravsky-kraj/' \
                      'okres-brno-mesto?priceFrom=&priceTo=&order=time_order_desc&submit=&page='+str(i)
                web_page_to_scrape = requests.get(url)
                soup = BeautifulSoup(web_page_to_scrape.content, 'html.parser')
                details2 = soup.find_all('div', class_='details')

                # pro kazdou stranku najdu lokalitu, cenu, velikost, id
                for item in details2:
                    header = item.find_all('h2', class_='header')[0]
                    text_h = header.get_text()
                    text_strip = text_h.strip()#[text_h.find('/n'):]

                    loc = text_strip[text_strip.find('Oblíbený')+8:].strip()

                    price = item.select_one('.price').get_text()
                    p1 = int(price[:price.find(' Kč')].replace('.',''))

                    size = item.select_one('.keys').get_text()[:-1]+'2'

                    link = item.select_one('p').get_text()

                    id = link[link.find('id/')+3:]
                    # zkontroluju, jestli uz id neni v predchozich datech, kdyz ne, pridam do listu
                    if id not in page.identifier:
                        page.lokalita.append(loc)
                        page.cena.append(p1)
                        page.velikost.append(size)
                        page.odkaz.append(link)
                        page.identifier.append(id)
                        self.cnt_new = self.cnt_new + 1

        # SREALITY
        elif page.page_name == 'sreality':
            for i in range(1,11):
                driver = webdriver.Chrome()
                url = "https://www.sreality.cz/hledani/prodej/byty/brno?stari=mesic&strana="+str(i)
                driver.get(url)
                soup = BeautifulSoup(driver.page_source,"html.parser")
                driver.quit()

                # pro kazdou stranku najdu lokalitu, cenu, velikost, id
                for title in soup.select(".text-wrap"):
                    # num = "https://www.sreality.cz" + title.select_one(".title").get('href')
                    # print(num)
                    size_2 = title.select_one('h2  span').get_text()[:-3]+" m2"
                    loc_2 = title.select_one("span [class='locality ng-binding']").get_text()
                    price_2 = title.select_one("span [class='norm-price ng-binding']").get_text().replace('\xa0','')[:-2]
                    link_2 = "https://www.sreality.cz" + title.select_one(".title").get('href')
                    id_2 = link_2[link_2.rfind("/")+1:]

                    # zkontroluju, jestli uz id neni v predchozich datech, kdyz ne, pridam do listu
                    if id_2 not in page.identifier:
                        page.lokalita.append(loc_2)
                        page.cena.append(price_2)
                        page.velikost.append(size_2)
                        page.odkaz.append(link_2)
                        page.identifier.append(id_2)
                        self.cnt_new = self.cnt_new + 1

        # REALITY BRNO
        elif page.page_name == 'reality':
            for i in range(1,11):
                url = 'https://www.reality-brno.net/prodej/byty/?strana='+str(i)
                web_page_to_scrape = requests.get(url)
                soup = BeautifulSoup(web_page_to_scrape.content, 'html.parser')
                details2 = soup.select('.nem_box')

                # pro kazdou stranku najdu lokalitu, cenu, velikost, id
                for item in details2:
                    title = item.select_one('h2').get_text()
                    loc_3 = title[title.rfind('Brno'):]
                    size_3 = item.select_one('.info_icons').get_text()
                    p_3 = item.select_one('.cena').get_text()[6:-5].replace(".","")
                    lnk_3 = item.select_one('h2 a').get('href')
                    link_3 = 'https://www.reality-brno.net/byty'+lnk_3
                    id_3 = lnk_3[lnk_3.find('id=')+3:lnk_3.find('&')]

                    # zkontroluju, jestli uz id neni v predchozich datech, kdyz ne, pridam do listu
                    if id_3 not in page.identifier:
                        page.lokalita.append(loc_3)
                        page.cena.append(p_3)
                        page.velikost.append(size_3)
                        page.odkaz.append(link_3)
                        page.identifier.append(id_3)
                        self.cnt_new = self.cnt_new + 1

                # page.export_to_csv()

        dates = [datetime.date.today()]*self.cnt_new
        page.date_created.extend(dates)
        print(self.cnt_new)

