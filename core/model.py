# -*- coding: utf-8 -*-


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


class Flight(object):
    fid = 0
    leave_time = 0
    arrive_time = 0
    from_ap = ""
    to_ap = ""
    plane = None
    period = 0

    def __init__(self, fid, leave_time, arrive_time, from_ap, to_ap, plane):
        self.fid = int(fid)
        self.leave_time = int(leave_time)
        self.arrive_time = int(arrive_time)
        self.from_ap = from_ap
        self.to_ap = to_ap
        self.plane = plane
        self.period = self.arrive_time - self.leave_time


class Solution(object):
    def __init__(self):
        self.flights = {}
        self.planes = {}
