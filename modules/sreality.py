import datetime
from bs4 import BeautifulSoup
from selenium import webdriver

from web_page import Page


class GetScraped(Page):
    def __init__(self, offer_type):

        super(GetScraped, self).__init__(page_name='sreality')
        self.req_offer_type = offer_type

        self.import_from_csv()
        self._scrape()
        self.export_to_csv()

        self.plural = 'bytu' if self.req_offer_type == 'byt' else 'domu'

        out_msg = '{0} novych {1} na {2}.'.format(self.cnt_new, self.plural, self.page_name)
        print(out_msg)

    def _scrape(self):
        # pocet novych nabidek
        self.cnt_new = 0

        for i in range(1, 11):
            driver = webdriver.Chrome()
            if self.req_offer_type == 'byt':
                url = "https://www.sreality.cz/hledani/prodej/byty/brno?stari=mesic&strana=" + str(i)
            elif self.req_offer_type == 'dum':
                url = "https://www.sreality.cz/hledani/prodej/domy/brno?stari=mesic&strana=" + str(i)
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            driver.quit()

            # pro kazdou stranku najdu lokalitu, cenu, velikost, id
            for title in soup.select(".text-wrap"):
                # num = "https://www.sreality.cz" + title.select_one(".title").get('href')
                # print(num)
                size_2 = (title.select_one('h2  span').get_text()[:-3] + " m2").replace('²', '')
                loc_2 = title.select_one("span [class='locality ng-binding']").get_text()
                price_2 = title.select_one("span [class='norm-price ng-binding']").get_text().replace('\xa0', '')[:-2]
                link_2 = "https://www.sreality.cz" + title.select_one(".title").get('href')
                id_2 = link_2[link_2.rfind("/") + 1:]

                # zmena ceny
                try:
                    i = self.identifier.index(id_2)
                    if self.cena[i] != price_2:
                        self.cena[i] = price_2
                        self.date_created[i] = datetime.date.today()

                    continue

                # nova nabidka
                except ValueError:
                    self.lokalita.append(loc_2)
                    self.cena.append(price_2)
                    self.velikost.append(size_2)
                    self.odkaz.append(link_2)
                    self.identifier.append(id_2)
                    self.cnt_new += 1

            dates = [datetime.date.today()] * self.cnt_new
            self.date_created.extend(dates)

            offer_types = [self.req_offer_type] * self.cnt_new
            self.offer_type.extend(offer_types)

