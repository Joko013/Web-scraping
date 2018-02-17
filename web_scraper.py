import csv
import requests
from bs4 import BeautifulSoup
from selenium import webdriver


import plotly.plotly as py
import plotly.graph_objs as go


# bezrealitky sreality reality


class Page():
    
    def __init__(self,page_name=None):
        self._page_name = page_name
        self._file_name = 'data_'+self._page_name+'.csv'       
    
        #import dat z csv
    def import_from_csv(self):
        self._lokalita = []
        self._cena = []
        self._velikost = []
        self._odkaz = []
        self._identifier = []
        
        #try pro pripad, ze soubor neexistuje 
        try:            
            with open(self._file_name, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=';', quotechar='|')
                for row in reader:
                    self._lokalita.append(row[0])
                    self._cena.append(row[1])
                    self._velikost.append(row[2])
                    self._odkaz.append(row[3])
                    self._identifier.append(row[4])
        except FileNotFoundError:
            pass
        
        #export dat do csv   
    def export_to_csv(self):
        with open(self._file_name, 'w') as csvfile:
            for (loc,cen,vel,odk,ide) in zip(self._lokalita, self._cena, self._velikost, self._odkaz, self._identifier):
                    csvfile.write(loc+';'+str(cen)+';'+vel+';'+odk+';'+str(ide)+'\n')
    
    
        #vlastni scraping s imp i exp - 3 moznosti pro 3 weby (ruzne tagy na kazdem webu)
    def scrape_page(self):
        
        self.import_from_csv()
        
        #pocet novych nabidek
        self.cnt_new = 0
        

              
        # BEZREALITKY
        if self._page_name == 'bezrealitky':
            for i in range(1,11):
                url = 'https://www.bezrealitky.cz/vypis/nabidka-prodej/byt/jihomoravsky-kraj/okres-brno-mesto?priceFrom=&priceTo=&order=time_order_desc&submit=&page='+str(i)
                page = requests.get(url)
                soup = BeautifulSoup(page.content, 'html.parser')
                details2 = soup.find_all('div', class_='details')

                #pro kazdou stranku najdu lokalitu, cenu, velikost, id
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
                    #zkontroluju, jestli uz id neni v predchozich datech, kdyz ne, pridam do listu
                    if id not in self._identifier:
                        self._lokalita.append(loc)
                        self._cena.append(p1)
                        self._velikost.append(size)
                        self._odkaz.append(link)
                        self._identifier.append(id)
                        self.cnt_new = self.cnt_new + 1
        
        #SREALITY
        elif self._page_name == 'sreality':
            for i in range(1,11):
                driver = webdriver.Chrome()
                url = "https://www.sreality.cz/hledani/prodej/byty/brno?stari=mesic&strana="+str(i)
                driver.get(url)
                soup = BeautifulSoup(driver.page_source,"html.parser")
                driver.quit()

                #pro kazdou stranku najdu lokalitu, cenu, velikost, id
                for title in soup.select(".text-wrap"):
                #num = "https://www.sreality.cz" + title.select_one(".title").get('href')
                #print(num)
                    size_2 = title.select_one('h2  span').get_text()[:-3]+" m2"
                    loc_2 = title.select_one("span [class='locality ng-binding']").get_text()
                    price_2 = title.select_one("span [class='norm-price ng-binding']").get_text().replace('\xa0','')[:-2]
                    link_2 = "https://www.sreality.cz" + title.select_one(".title").get('href')
                    id_2 = link_2[link_2.rfind("/")+1:]

                    #zkontroluju, jestli uz id neni v predchozich datech, kdyz ne, pridam do listu
                    if id_2 not in self._identifier:
                        self._lokalita.append(loc_2)
                        self._cena.append(price_2)
                        self._velikost.append(size_2)
                        self._odkaz.append(link_2)
                        self._identifier.append(id_2)
                        self.cnt_new = self.cnt_new + 1        
        
        # REALITY BRNO
        elif self._page_name == 'reality':            
            for i in range(1,11):
                url = 'https://www.reality-brno.net/prodej/byty/?strana='+str(i)
                page = requests.get(url)
                soup = BeautifulSoup(page.content, 'html.parser')
                details2 = soup.select('.nem_box')

                #pro kazdou stranku najdu lokalitu, cenu, velikost, id
                for item in details2:
                    title = item.select_one('h2').get_text()
                    loc_3 = title[title.rfind('Brno'):]
                    size_3 = item.select_one('.info_icons').get_text()
                    p_3 = item.select_one('.cena').get_text()[6:-5].replace(".","")
                    lnk_3 = item.select_one('h2 a').get('href')
                    link_3 = 'https://www.reality-brno.net/byty'+lnk_3
                    id_3 = lnk_3[lnk_3.find('id=')+3:lnk_3.find('&')]

                    #zkontroluju, jestli uz id neni v predchozich datech, kdyz ne, pridam do listu
                    if id_3 not in self._identifier:
                        self._lokalita.append(loc_3)
                        self._cena.append(p_3)
                        self._velikost.append(size_3)
                        self._odkaz.append(link_3)
                        self._identifier.append(id_3)
                        self.cnt_new = self.cnt_new + 1 
        
        self.export_to_csv()
        
        
    @property
    def lokalita(self):
        return self._lokalita
    @property
    def cena(self):
        return self._cena
    @property
    def velikost(self):
        return self._velikost
    @property
    def odkaz(self):
        return self._odkaz
    @property
    def identifier(self):
        return self._identifier
        
       
        
       
                   
         

