# -*- coding: utf-8 -*-

from core import test
from utils import input, output

if __name__ == '__main__':
    pass
    # content = scrapy.retrieve_data(URL)
    # print scrapy.extract_price(content)
    # print(input.csv('samples/Schedules.csv'))
    solution = test.SolutionTest()
    print(input.csv_input('samples/Aircrafts.csv', 'samples/Schedules.csv', solution))
    solution.calculate()
    output.csv_output('ans/ans2.csv', solution)
    # print(len(solution.scheduled))
    # print((1461468000 - 1461294000) / 60)
    # print(delay, len(scheduled))
