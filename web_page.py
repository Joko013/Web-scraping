# This Python file uses the following encoding: utf-8

import csv
import os


class Page:

    def __init__(self, page_name=None):
        self.page_name = page_name
        self._file_name = 'data_' + self.page_name + '.csv'
        self._path = 'C:\\Users\\admin\\Web_Scraping\\' + self._file_name

    def import_from_csv(self):
        """
        Import previous data from CSV
        :return: None
        """

        self.lokalita = []
        self.cena = []
        self.velikost = []
        self.odkaz = []
        self.identifier = []
        self.date_created = []

        # try pro pripad, ze soubor neexistuje
        try:
            with open(self._path, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=';', quotechar='|')
                for row in reader:
                    self.lokalita.append(row[0])
                    self.cena.append(row[1])
                    self.velikost.append(row[2])
                    self.odkaz.append(row[3])
                    self.identifier.append(row[4])
                    self.date_created.append(row[5])
        except FileNotFoundError:
            pass

    def export_to_csv(self):
        """
        Export page data to CSV file
        :return: None
        """
        with open(self._path, 'w') as csvfile:
            zipped = zip(self.lokalita, self.cena,
                          self.velikost, self.odkaz,
                          self.identifier, self.date_created)
            for (loc, cen, vel, odk, ide, dte) in zipped:
                csvfile.write(loc+';'+str(cen)+';'+vel+';'+odk+';'+str(ide)+';'+str(dte)+'\n')
