# -*- coding: utf-8 -*-
from .read_csv import *


def hi():
    print("hello world")


def csv_input(plane_src, flight_src, solution):
    ct1 = load_planes(plane_src, solution)
    ct2 = load_flights(flight_src, solution)
    return ct1, ct2
