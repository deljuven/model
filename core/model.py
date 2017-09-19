# -*- coding: utf-8 -*-

from _datetime import datetime
from collections import defaultdict
from enum import Enum

LIMIT_START, LIMIT_END, LIMIT_FROM, LIMIT_TO, DURATION = 1461348000, 1461358800, 180, 316, 18000

TIME_START, TIME_END, SLOT, = 1461294000, 1461468000, 600

SIZE = DURATION // SLOT


class Plane(object):
    pid = ""
    category = ""
    avail_start = 0
    avail_end = 0
    size = 0
    init_ap = ""

    def __init__(self, pid, category, start, end, size, ap):
        self.pid = pid
        self.category = category
        self.avail_start = int(start)
        self.avail_end = int(end)
        self.size = int(size)
        self.init_ap = ap


class Status(Enum):
    in_ap = 0
    out_ap = 1


class PlaneStatus(object):
    plane = None
    status = Status
    current = ""

    def __init__(self, plane, status, current):
        self.plane = plane
        self.status = status
        self.current = current


class Flight(object):
    fid = 0
    leave_time = 0
    arrive_time = 0
    from_ap = ""
    to_ap = ""
    period = 0
    required_category = ""

    def __init__(self, fid, leave_time, arrive_time, from_ap, to_ap, required_category):
        self.fid = int(fid)
        self.leave_time = int(leave_time)
        bias = self.leave_time % 300
        if bias:
            self.leave_time -= bias
        self.arrive_time = int(arrive_time)
        bias = self.arrive_time % 300
        if bias:
            self.arrive_time -= bias
        self.from_ap = from_ap
        self.to_ap = to_ap
        self.period = (self.arrive_time - self.leave_time) // 300
        self.required_category = required_category

    def value(self):
        return {'fid': self.fid,
                'leave_time': datetime.utcfromtimestamp(self.leave_time).strftime('%m/%d/%y %H:%M'),
                'arrive_time': datetime.utcfromtimestamp(self.arrive_time).strftime('%m/%d/%y %H:%M'),
                'from_ap': self.from_ap, 'to_ap': self.to_ap}

    def copy(self):
        return Flight(self.fid, self.leave_time, self.arrive_time, self.from_ap, self.to_ap, self.required_category)


class Flight_Scheduled(object):
    old_flight = None
    new_flight = None
    old_plane = None
    new_plane = None
    delay = 0

    def __init__(self, old_flight, old_plane, new_flight, new_plane):
        self.old_flight = old_flight
        self.new_flight = new_flight
        self.old_plane = old_plane
        self.new_plane = new_plane
        self.delay = (new_flight.leave_time - old_flight.leave_time) // 60

    def value(self):
        'fid', 'leave_time', 'arrive_time', 'from_ap', 'to_ap', 'category', 'pid', 'new_category',
        'new_pid', 'new_leave', 'new_arrive', 'delay'
        return {'fid': self.old_flight.fid,
                'leave_time': datetime.utcfromtimestamp(self.old_flight.leave_time).strftime('%m/%d/%y %H:%M'),
                'arrive_time': datetime.utcfromtimestamp(self.old_flight.arrive_time).strftime('%m/%d/%y %H:%M'),
                'from_ap': self.old_flight.from_ap, 'to_ap': self.old_flight.to_ap,
                'category': self.old_flight.required_category,
                'pid': self.old_plane, 'new_category': self.old_flight.required_category, 'new_pid': self.new_plane,
                'new_leave': datetime.utcfromtimestamp(self.new_flight.leave_time).strftime('%m/%d/%y %H:%M'),
                'new_arrive': datetime.utcfromtimestamp(self.new_flight.arrive_time).strftime('%m/%d/%y %H:%M'),
                'delay': self.delay}


class Solution(object):
    planes = {}
    flights = {}
    flight_plane = {}
    planes_of_ap = defaultdict(list)
    flights_from_ap = defaultdict(list)
    flights_in_order = []

    updated_flights = {}

    def __init__(self):
        self.planes = {}
        self.flights = {}
        self.flight_plane = {}
        self.flights_in_order = []
        self.planes_of_ap = defaultdict(list)
        self.flights_from_ap = defaultdict(list)
        self.flights_to_ap = defaultdict(list)

    def prepare_planes(self):
        for plane in self.planes.values():
            self.planes_of_ap[plane.init_ap].append(plane)
        for x in self.planes_of_ap.values():
            x.sort(key=lambda p: p.avail_start)

    def prepare_flights(self):
        for flight in self.flights.values():
            self.flights_from_ap[flight.from_ap].append(flight)
            self.flights_to_ap[flight.to_ap].append(flight)
            self.updated_flights[flight.fid] = flight.copy()
        for x in self.flights_from_ap.values():
            x.sort(key=lambda f: f.leave_time)
        for x in self.flights_to_ap.values():
            x.sort(key=lambda f: f.arrive_time)

    def filter_plane(self, plane):
        return True

    def calculate(self):
        return
