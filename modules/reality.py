import datetime
import requests
from bs4 import BeautifulSoup

from web_page import Page


class GetScraped(Page):
    def __init__(self):

        super(GetScraped, self).__init__(page_name='reality')

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
            url = 'https://www.reality-brno.net/prodej/byty/?strana=' + str(i)
            web_page_to_scrape = requests.get(url)
            soup = BeautifulSoup(web_page_to_scrape.content, 'html.parser')
            details2 = soup.select('.nem_box')

            # pro kazdou stranku najdu lokalitu, cenu, velikost, id
            for item in details2:
                title = item.select_one('h2').get_text()
                loc_3 = title[title.rfind('Brno'):]
                size_3 = item.select_one('.info_icons').get_text()
                p_3 = item.select_one('.cena').get_text()[6:-5].replace(".", "")
                lnk_3 = item.select_one('h2 a').get('href')
                link_3 = 'https://www.reality-brno.net/byty' + lnk_3
                id_3 = lnk_3[lnk_3.find('id=') + 3:lnk_3.find('&')]

                # zmena ceny
                try:
                    i = self.identifier.index(id_3)
                    if self.cena[i] != p_3:
                        self.cena[i] = p_3
                        self.date_created[i] = datetime.date.today()

                        new_this_page += 1

                        continue
                # nova nabidka
                except ValueError:
                    self.lokalita.append(loc_3)
                    self.cena.append(p_3)
                    self.velikost.append(size_3)
                    self.odkaz.append(link_3)
                    self.identifier.append(id_3)
                    self.cnt_new += 1
                    new_this_page += 1

                break

            dates = [datetime.date.today()] * self.cnt_new
            self.date_created.extend(dates)

