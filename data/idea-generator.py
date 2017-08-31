"""Module that scrapes concept data to be used by the idea generator

Runs through a number of "Scrapers" that take concept data, such as magic 
types, locations, and animals, and saves these in JSON files to be 
loaded into the database as fixtures.
"""

import json
import os
import requests
from bs4 import BeautifulSoup

class Scraper:
    """Abstract class for a scraper object. Must implement a scrape method."""
    def scrape(self):
        raise NotImplementedError('User must implement the scrape method')


class MagicScraper(Scraper):
    """Scrapes types of magic from http://powerlisting.wikia.com/wiki/Magic"""
    def __init__(self, source):
        """ Initialize with URL for scraper"""
        self.source = source

    def scrape(self):
        """Scrapes the types of magic from the URL and returns the list.

        :return : list types of magic
        """
        response = requests.get(self.source)
        soup = BeautifulSoup(response.text, 'html.parser')
        types = []
        list1 = soup.select('#Types_of_Magic')[0].findNext('ul')
        list2 = list1.findNext('ul')
        for item in list1.select('li a'):
            types.append(item.text)
        for item in list2.select('li a'):
            types.append(item.text)

        return types


class AnimalScraper(Scraper):
    """Scrapes animals from Wikipedia."""
    def __init__(self, source):
        """Initialize with URL for scraper"""
        self.source = source

    def scrape(self):
        """Scrapes the names of animals from the URL and returns the list.

        :return : list names of animals
        """
        response = requests.get(self.source)
        soup = BeautifulSoup(response.text, 'html.parser')
        animals = []
        element = soup.select('#By_taxon_or_species')[0].parent
        next_element = element.next_sibling.next_sibling
        while next_element.select('#Names_for_males.2C_females.2C_young.2C_and_groups') == []:
            for item in next_element.select('li a'):
                animals.append(item.text)
            next_element = next_element.next_sibling.next_sibling

        return animals


class CreatureScraper(Scraper):
    """Scrapes mythical creatures from Wikipedia."""
    def __init__(self, base_url):
        """Initialize with base URL for scraper"""
        self.base_url = base_url

    def scrape(self):
        """Scrapes the lists of creatures from the lists from A-Z

        :return : list of mythical creatures
        """
        creatures = []
        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            response = requests.get(self.base_url + '_(' + letter + ')')
            soup = BeautifulSoup(response.text, 'html.parser')
            content = soup.select('#mw-content-text')[0]
            for item in content.select('li'):
                # creature = {}
                # creature['link'] = item.select('a')[0].get('href') if item.select('a') else ''
                # creature['name'] = item.text
                creatures.append(item.text.encode('ascii', errors='ignore').decode())

        return creatures


class EventScraper(Scraper):
    """Scrapes historical events from URL."""
    def __init__(self, source):
        """Initialize with source"""
        self.source = source

    def scrape(self):
        """Scrapes the URL for list of historical events

        :return : list of events
        """
        response = requests.get(self.source)
        soup = BeautifulSoup(response.text, 'html.parser')
        events = []
        for item in soup.select('.listItem__title'):
            if item.text.strip() != '':
                events.append(item.text)

        return events


class ScraperRunner:
    """Acts as the runner and controls the individual scrapers"""
    def __init__(self):
        self.data = []

    def run_scrapers(self):
        """Instantiates scrapers with sources and runs scrape."""
        magic_types = MagicScraper('http://powerlisting.wikia.com/wiki/Magic').scrape()
        self.add_fixture('Magic', magic_types)
        animals = AnimalScraper(
            'https://en.wikipedia.org/wiki/List_of_animals_by_common_name'
        ).scrape()
        self.add_fixture('Animals', animals)
        creatures = CreatureScraper(
            'https://en.wikipedia.org/wiki/List_of_legendary_creatures'
        ).scrape()
        self.add_fixture('Creatures', creatures)
        events = EventScraper(
            'http://www.ranker.com/list/most-important-historical-events-of-the-20th-century/mwahahahaha'
        ).scrape()
        self.add_fixture('Events', events)

        self.save_fixture()

    def add_fixture(self, category, items):
        """Adds to JSON object"""
        data = []
        for item in items:
            data.append({
                "model": "ideas.concept",
                "fields": {
                    "category": category,
                    "label": item
                }
            })

        self.data += data

    def save_fixture(self):
        """Saves to JSON fixture file to be loaded into the Django database."""
        with open('../ideas/fixtures/concepts.json', 'w') as handle:
            json.dump(self.data, handle)


if __name__ == '__main__':
    scraper = ScraperRunner()
    scraper.run_scrapers()
