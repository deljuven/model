# -*- coding: utf-8 -*-
import csv

from core.model import *


def load_planes(src, solution):
    count = 0
    with open(src, newline='', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            count += 1
            pid, category, start, end, size, ap = row[0], row[1], row[2], row[3], row[5], row[4]
            solution.planes[pid] = Plane(pid, category, start, end, size, ap)
    return count


def load_flights(src, solution):
    count = 0
    with open(src, newline='', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            fid, leave_time, arrive_time, from_ap, to_ap, plane = row[0], row[1], row[2], row[3], row[4], row[6]
            if plane not in solution.planes:
                continue
            plane = solution.planes[plane]
            count += 1
            solution.flights[fid] = Flight(fid, leave_time, arrive_time, from_ap, to_ap, plane)
    return count
