import datetime
from bs4 import BeautifulSoup
from selenium import webdriver

from web_page import Page


class GetScraped(Page):
    def __init__(self):

        super(GetScraped, self).__init__(page_name='sreality')

        self.import_from_csv()
        self._scrape()
        self.export_to_csv()

        out_msg = '{0} new listings for {1} page.'.format(self.cnt_new, self.page_name)
        print(out_msg)

    def _scrape(self):
        # pocet novych nabidek
        self.cnt_new = 0

        for i in range(1, 11):
            new_this_page = 0
            driver = webdriver.Chrome()
            url = "https://www.sreality.cz/hledani/prodej/byty/brno?stari=mesic&strana=" + str(i)
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            driver.quit()

            # pro kazdou stranku najdu lokalitu, cenu, velikost, id
            for title in soup.select(".text-wrap"):
                # num = "https://www.sreality.cz" + title.select_one(".title").get('href')
                # print(num)
                size_2 = title.select_one('h2  span').get_text()[:-3] + " m2"
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

                        new_this_page += 1

                        continue
                # nova nabidka
                except ValueError:
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

