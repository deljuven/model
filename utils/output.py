# -*- coding: utf-8 -*-
import csv


def csv_output(target, solution):
    with open(target, 'w') as csv_file:
        fieldnames = ['fid', 'leave_time', 'arrive_time', 'from_ap', 'to_ap', 'category', 'pid', 'new_category',
                      'new_pid', 'new_leave', 'new_arrive', 'delay']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, lineterminator='\n')

        writer.writeheader()
        for fid in solution.flights_in_order:
            writer.writerow(solution.updated_flights[fid].value())
