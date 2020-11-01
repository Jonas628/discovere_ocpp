"Simulate a clock that runs at a certain speed"
import asyncio
import os
import math
import time
simtime = 0
_year = 2020
_month = 10

try:
    TIMELAPSE = int(os.environ["TIMELAPSE"])
except KeyError:
    TIMELAPSE = 1000


def clock():
    global simtime, _year, _month
    while True:
        time.sleep(1)
        simtime += 1*TIMELAPSE
        if simtime > 2592000:
            simtime -= 2592000
            _month += 1
            if _month == 12:
                _month -= 11
                _year += 1


def timestamp():
    day = 1 + math.floor(simtime/86400)
    remaining = simtime % 86400
    hours = math.floor(remaining/3600)
    remaining = remaining % 3600
    minutes = math.floor(remaining/60)
    seconds = remaining % 60
    return f"{_year}-{_month}-{day}::{hours}:{minutes}:{seconds}"


def hours():
    return math.floor((simtime % 86400)/3600)


def minutes():
    return math.floor(((simtime % 86400) % 3600)/60)


def seconds():
    return math.floor(((simtime % 86400) % 3600) % 60)


loop = asyncio.get_event_loop()
# run in background - None defaults to current loop executor
loop.run_in_executor(None, clock)
