# -*- coding: utf-8 -*-
import csv

from core.model import *


def load_planes(src, solution):
    count = 0
    with open(src, newline='', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            pid, category, start, end, size, ap = row[0], row[1], row[2], row[3], row[5], row[4]
            plane = Plane(pid, category, start, end, size, ap)
            if solution.filter_plane(plane):
                count += 1
                solution.planes[pid] = plane
    return count


def load_flights(src, solution):
    count = 0
    with open(src, newline='', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            fid, leave_time, arrive_time, from_ap, to_ap, plane, category = \
                row[0], row[1], row[2], row[3], row[4], row[6], row[5]
            if plane not in solution.planes:
                continue
            # plane = solution.planes[plane]
            count += 1
            flight = Flight(fid, leave_time, arrive_time, from_ap, to_ap, category)
            solution.flights[flight.fid] = flight
            solution.flight_plane[flight.fid] = plane
            solution.flights_in_order.append(flight.fid)
    return count
