# -*- coding: utf-8 -*-

from .model import *


class Solution1(Solution):
    waiting_lists = defaultdict(list)
    plane_status = {}

    def __init__(self):
        super().__init__()

    def filter_plane(self, plane):
        return plane.category == "9"

    def update_plane_status(self, pid, status, ap):
        ps = self.plane_status[pid]
        ps.status = status
        ps.current = ap


class SolidSolution(Solution):
    slots = defaultdict(list)
    scheduled = {}
    delay = 0

    def __init__(self):
        super().__init__()

    def filter_plane(self, plane):
        return plane.category == "9"

    def generate_slots(self):
        for fid, flight in self.flights.items():
            # for t in range(TIME_START, TIME_END):
            start = (flight.leave_time - TIME_START) // SLOT
            end = start + SIZE
            self.slots[fid] = [start, end, start, start + flight.period]

    def is_schedule_valid(self):
        for fid, flight in self.flights.items():
            time_slot = -1
            if flight.to_ap == "OVS":
                time_slot = self.slots[fid][3]
            elif flight.from_ap == "OVS":
                time_slot = self.slots[fid][2]
            if LIMIT_FROM <= time_slot < LIMIT_TO:
                return False
            if not self.plane_valid(fid, self.slots[fid][2] * SLOT + TIME_START, self.slots[fid][3] * SLOT + TIME_START,
                                    flight.from_ap):
                return False
        return True

    def plane_valid(self, fid, start, end, at):
        plane = self.planes[self.flight_plane[fid]]
        if plane.avail_start <= start < end <= plane.avail_end and plane in self.planes_of_ap[at]:
            return True
        return False

    def compute_delay(self):
        delay = 0
        for fid, flight in self.flights.items():
            offset = self.slots[fid][2] - self.slots[fid][0]
            delay += offset
            flight_new = flight.copy()
            flight_new.leave_time = self.slots[fid][2] * SLOT + TIME_START
            flight_new.arrive_time = flight_new.leave_time + flight.period * 300
            self.scheduled[fid] = Flight_Scheduled(flight, self.flight_plane[fid], flight_new, self.flight_plane[fid])
        return delay * SLOT // 60

    def update_slots(self, step):
        index = len(self.flights) - 1
        for x in self.flights.keys():
            tmp = pow(SIZE, index)
            pos = step // tmp
            self.slots[x][2] += pos
            if step >= tmp:
                step -= pos * tmp
            index -= 1

    def iterate_all(self):
        self.generate_slots()
        fin = pow(SIZE, len(self.flights))
        delay = TIME_END - TIME_START
        failed, count = 0, 1
        print(fin)
        for step in range(fin):
            # self.update_slots(step)
            # if self.is_schedule_valid():
            #     pass
            # tmp = self.compute_delay()
            # if delay > tmp:
            #     delay = tmp
            #     self.update_schedule()
            # else:
            #     failed += 1
            #     if failed > pow(10, count):
            #         print(failed)
            #         count += 1
            pass
        print("fin")

        self.delay = delay

    def update_schedule(self):
        for x in self.slots:
            self.scheduled[x] = list(self.slots[x])

    def get_result(self):
        return self.scheduled

    def calculate(self):
        self.iterate_all()
        return self.delay, self.get_result()
