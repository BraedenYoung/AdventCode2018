from input_decorator import has_input

from collections import defaultdict
from datetime import datetime
from enum import Enum
import re


SAMPLE = '''
[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up
'''


class Event(Enum):
    START = 0
    SLEEP = 1
    WAKE = 2


class AuditLog(tuple):
    def guard_id(self):
        return self[1]

    def date_time(self):
        return self[0]

    def event(self):
        return self[2]


class Day(object):
    def __init__(self, date_time, guard_id):
        self._lst = [date_time, guard_id]
        self._lst.extend([0] * 60)

    def __getitem__(self, item):
        return self._lst[item]

    def __str__(self):
        return '|'.join(map(str, self._lst))

    def guard_id(self):
        return self[1]

    def date_time(self):
        return self[0]

    def set_sleep(self, start, stop):
        self._lst[start+2:stop+2] = [1] * (stop - start)

    def minutes_sleeping(self):
        return sum(self[2:])

    def minutes(self):
        return self._lst[2:]


@has_input
def part_one(input):
    audit_log = create_auditlog(input)
    schedule = create_schedule(audit_log)

    sleep_hours, sleepy_guard_id = find_sleepy_guard(schedule)
    max_minute = find_sleep_minute(schedule, sleepy_guard_id)

    print '{0}, minute: {1}'.format(sleepy_guard_id, max_minute)


def create_auditlog(input):
    datetime_pattern = re.compile('(\[.*\])')
    info_pattern = re.compile('(\].*)')
    guard_id_pattern = re.compile('(Guard #\d+)')
    begins_shift_pattern = re.compile('begins\sshift')
    falls_asleep_pattern = re.compile('falls\sasleep')
    wakes_up_pattern = re.compile('wakes\sup')

    audit_log = []

    for line in input.strip().splitlines():
        datetime_stamp = datetime_pattern.search(line).group(1)[1:-1]
        datetime_parsed = datetime.strptime(datetime_stamp, '%Y-%m-%d %H:%M')

        event_info = info_pattern.search(line).group(1)[1:]
        guard_id = guard_id_pattern.search(event_info)
        if guard_id:
            guard_id = guard_id.group(1)
        begins_shift_event = begins_shift_pattern.search(event_info)
        if begins_shift_event:
            event = Event.START
        falls_asleep_event = falls_asleep_pattern.search(event_info)
        if falls_asleep_event:
            event = Event.SLEEP
        wakes_up_event = wakes_up_pattern.search(event_info)
        if wakes_up_event:
            event = Event.WAKE

        audit_log.append(AuditLog((datetime_parsed, guard_id, event)))

    audit_log.sort(key=lambda a: a[0])
    return audit_log


def create_schedule(audit_log):
    schedule = []
    started_sleeping = -1
    for audit in audit_log:
        if audit.event() == Event.START:
            schedule.append(Day(audit.date_time(), audit.guard_id()))
            continue

        if audit.event() == Event.SLEEP:
            started_sleeping = audit.date_time().minute
            continue

        curr_day = schedule[-1]
        curr_day.set_sleep(started_sleeping, audit.date_time().minute)

    return schedule


def find_sleepy_guard(schedule):
    guard_map = defaultdict(0)
    for day in schedule:
        guard_map[day.guard_id()] += day.minutes_sleeping()

    max_sleep = (0, '')
    for guard_id, sleep in guard_map.iteritems():
        if sleep > max_sleep[0]:
            max_sleep = (sleep, guard_id)
    return max_sleep


def find_sleep_minute(schedule, guard_id):
    minutes = defaultdict(0)
    max = 0
    max_minute = -1
    for day in schedule:
        if day.guard_id() != guard_id:
            continue

        for index, minute in enumerate(day.minutes()):
            minutes[index] += minute
            if minutes[index] > max:
                max = minutes[index]
                max_minute = index

    return max_minute


@has_input
def part_two(input):
    audit_log = create_auditlog(input)
    schedule = create_schedule(audit_log)

    checked_guards = set()
    max_minute = 0
    sleepy_guard_id = ''

    for day in schedule:
        if day.guard_id() in checked_guards:
            continue

        checked_guards.add(day.guard_id())
        curr_max = find_sleep_minute(schedule, day.guard_id())
        if curr_max > max_minute:
            max_minute = curr_max
            sleepy_guard_id = day.guard_id()

    print '{0}, minute: {1}'.format(sleepy_guard_id, max_minute)
