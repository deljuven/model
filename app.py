# -*- coding: utf-8 -*-

from core.model import Solution
from utils import input

if __name__ == '__main__':
    pass
    # content = scrapy.retrieve_data(URL)
    # print scrapy.extract_price(content)
    # print(input.csv('samples/Schedules.csv'))
    solution = Solution()
    print(input.csv_input('samples/Aircrafts.csv', 'samples/Schedules.csv', solution))
