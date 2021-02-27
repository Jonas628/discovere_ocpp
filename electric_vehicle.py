import random
import asyncio
import time
import os


class ElectricVehicle(object):

    def __init__(self, charge_point, name="car"):
        self.name = name
        self.cp = charge_point
        self.capacity = random.randint(30 * 3600, 80 * 3600)  # in kWs
        self.soc = int(random.random()*self.capacity)  # initial soc
        self.consumption = random.randint(15 * 36, 25 * 36)  # in kWs/km
        try:
            self.timelapse = os.environ["TIMELAPSE"]
        except KeyError:
            print("$TIMELAPSE not defined, set to 1...")
            self.timelapse = 1

    async def run(self):
        while True:
            await self.drive()
            await self.sleep()
            if self.soc < self.capacity*0.5:
                await self.charge()

    async def drive(self):
        print("start driving...")
        start = time.time()
        duration = random.randint(1, 10)
        distance = duration * random.randint(25, 50)  # distance to drive in km
        duration = int((distance / 50) * 3600) / self.timelapse  # duration in seconds when driving with 50 km/h
        energy_consumed = distance * self.consumption
        self.soc -= energy_consumed
        if not self.soc > 0:
            print("The car has died...")
        while time.time() - start < duration:
            await asyncio.sleep(0.01)
        print(f"drove for {duration} seconds.")

    async def sleep(self):
        print("sleeping...")
        # sleep between a minute and an hour
        start = time.time()
        duration = random.randint(60, 3600) / self.timelapse
        while time.time() - start < duration:
            await asyncio.sleep(0.01)
        print(f"slept {duration} seconds")

    async def charge(self):
        print("want to charge now")
        await self.cp.charge(self)
        print(self.soc)
