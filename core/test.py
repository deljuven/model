# -*- coding: utf-8 -*-

from .model import *


class SolutionTest(Solution):
    scheduled = {}
    scheduled_plane = {}

    plane_before_limit = []
    plane_before_limit_by_category = defaultdict(list)
    plane_after_limit = []
    plane_after_limit_by_category = defaultdict(list)

    def __init__(self):
        super().__init__()

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

    def before_limit(self):
        self.plane_before_limit = {}
        for plane in self.planes_of_ap["OVS"]:
            self.plane_before_limit[plane.pid] = 1
        for fid, flight in self.flights.items():
            if fid not in self.flight_plane:
                continue
            if flight.to_ap == "OVS" and flight.arrive_time < LIMIT_START:
                self.plane_before_limit[self.flight_plane[fid]] = 1
            elif flight.from_ap == "OVS" and flight.leave_time < LIMIT_START:
                self.plane_before_limit[self.flight_plane[fid]] = 0
        for p, exist in self.plane_before_limit.items():
            plane = self.planes[p]
            if exist:
                self.plane_before_limit_by_category[plane.category].append(plane)
                # self.plane_before_limit_by_category[plane.category].append(p)

    def after_limit(self):
        self.plane_after_limit = {}
        for plane in self.planes_of_ap["OVS"]:
            self.plane_after_limit[plane.pid] = 1
        for fid, flight in self.flights.items():
            if fid not in self.flight_plane:
                continue
            if flight.to_ap == "OVS" and flight.arrive_time < LIMIT_START:
                self.plane_after_limit[self.flight_plane[fid]] = 1
            elif flight.from_ap == "OVS" and flight.leave_time < LIMIT_START:
                self.plane_after_limit[self.flight_plane[fid]] = 0
        for p, exist in self.plane_after_limit.items():
            plane = self.planes[p]
            if exist > 0:
                self.plane_after_limit_by_category[plane.category].append(plane)
                # self.plane_after_limit_by_category[plane.category].append(p)

    def schedule(self):
        self.prepare_planes()
        self.prepare_flights()
        self.before_limit()
        self.after_limit()
        left_after_limit_start = {}
        left_in_order = []
        pending_list = {}
        pending_in_order = []
        for fid, flight in self.flights.items():
            if fid not in self.flight_plane:
                continue
            if flight.to_ap == "OVS":
                if flight.arrive_time < LIMIT_START:
                    self.scheduled[fid] = flight.copy()
                    self.scheduled_plane[fid] = self.flight_plane[fid]
                else:
                    pending_list[fid] = flight.copy()
                    pending_in_order.append(pending_list[fid])
            elif flight.from_ap == "OVS":
                if flight.leave_time < LIMIT_START:
                    self.scheduled[fid] = flight.copy()
                    self.scheduled_plane[fid] = self.flight_plane[fid]
                else:
                    left_after_limit_start[fid] = flight.copy()
                    left_in_order.append(left_after_limit_start[fid])

        left_in_order.sort(key=lambda f: f.leave_time)
        pending_in_order.sort(key=lambda f: f.arrive_time)

        for idx, flight in enumerate(left_in_order):
            fid = flight.fid
            waitings = self.plane_after_limit_by_category[flight.required_category]
            if waitings:
                if fid in self.scheduled:
                    print(fid)
                candidate = waitings.pop()
                self.scheduled[fid] = flight.copy()
                self.scheduled_plane[fid] = candidate.pid
                left_after_limit_start[fid] = None
                left_in_order[idx] = None
                # self.flight_plane[]

        for idx, flight in enumerate(pending_in_order):
            if flight:
                fid = flight.fid
                for ix, f in enumerate(left_in_order):
                    if f and f.required_category == flight.required_category:
                        left = f.fid
                        self.scheduled[left] = flight.copy()
                        self.scheduled_plane[left] = self.flight_plane[fid]
                        self.scheduled[left].leave_time = max(f.leave_time, LIMIT_END + 45 * 60)
                        self.scheduled[left].arrive_time = self.scheduled[left].leave_time + \
                                                           self.scheduled[left].period * 300
                        left_in_order[ix] = None
                        break

        for idx, flight in enumerate(pending_in_order):
            if flight:
                fid = flight.fid
                self.scheduled[fid] = flight.copy()
                self.scheduled_plane[fid] = self.flight_plane[fid]
                self.scheduled[fid].arrive_time = max(flight.arrive_time, LIMIT_END)
                self.scheduled[fid].leave_time = self.scheduled[fid].arrive_time - flight.period * 300
                pending_in_order[idx] = None

    def calculate(self):
        self.schedule()
        for fid, flight_new in self.scheduled.items():
            if fid not in self.flights:
                print(fid, self.flight_plane)
            self.updated_flights[fid] = Flight_Scheduled(self.flights[fid], self.flight_plane[fid], flight_new,
                                                         self.scheduled_plane[fid])
