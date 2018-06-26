# This Python file uses the following encoding: utf-8

import web_scraper
import web_page

if __name__ == '__main__':
    scrap = web_scraper.Scraper()
    pages = ['sreality', 'reality']  # , 'bezrealitky'

    for name in pages:
        p = web_page.Page(name)
        p.import_from_csv()

        scrap.scrape_page(p)
        p.export_to_csv()

