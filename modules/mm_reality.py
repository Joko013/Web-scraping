import datetime
from bs4 import BeautifulSoup
from selenium import webdriver

from web_page import Page


class GetScraped(Page):
    def __init__(self):
        
        super(GetScraped, self).__init__(page_name='mm_reality')

        self.import_from_csv()
        self._scrape()
        self.export_to_csv()

        out_msg = '{0} new listings for {1} page.'.format(self.cnt_new, self.page_name)
        print(out_msg)

    def _scrape(self):
        # pocet novych nabidek
        self.cnt_new = 0
        
        for i in range(1, 6):
            new_this_page = 0

            url = 'https://www.mmreality.cz/nemovitosti/hledani/?&filter%5BfCategory%5D%5B%5D=10&filter%5BfEstateType' \
                  '%5D=11&filter%5BfDisposition%5D%5B%5D=200&filter%5BfDisposition%5D%5B1%5D=55&filter%5BfDisposition' \
                  '%5D%5B2%5D=201&filter%5BfDisposition%5D%5B3%5D=56&filter%5BfDisposition%5D%5B4%5D=202&filter%5Bf' \
                  'Disposition%5D%5B5%5D=57&filter%5BfRegion%5D=116&filter%5BfDistrict%5D%5B%5D=3702&page=' + str(i)

            driver = webdriver.Chrome()
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            driver.quit()

            # pro kazdou stranku najdu lokalitu, cenu, velikost, id

            offers_list = soup.select('.offersList')[0]

            for offer in offers_list.select('article'):
                title = offer.find('a')['title']
                split_title = title.split(',')

                size_2 = split_title[1]
                loc_2 = split_title[-1]
                price_2 = offer.select('strong.price')[0].text
                link_2 = 'https://www.mmreality.cz' + offer.select('a')[0]['href']
                id_2 = offer.select('a')[0]['href'][:-1].split('/')[-1]

                # zkontroluju, jestli uz id neni v predchozich datech, kdyz ne, pridam do listu
                if id_2 not in self.identifier:
                    self.lokalita.append(loc_2)
                    self.cena.append(price_2)
                    self.velikost.append(size_2)
                    self.odkaz.append(link_2)
                    self.identifier.append(id_2)
                    self.cnt_new += 1
                    new_this_page += 1
            if new_this_page == 0:
                break

            dates = [datetime.date.today()] * self.cnt_new
            self.date_created.extend(dates)

