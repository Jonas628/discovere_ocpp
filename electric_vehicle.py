import random
import asyncio
import os

try:
    TIMELAPSE = int(os.environ["TIMELAPSE"])
except KeyError:
    TIMELAPSE = 1


class ElectricVehicle(object):

    def __init__(self, chargepoint, name="car"):
        self.name = name
        self.chargepoint = chargepoint
        self.capacity = random.randint(30 * 3600, 80 * 3600)  # in kWs
        self.soc = int(random.random()*self.capacity)  # initial soc
        self.consumption = random.randint(15 * 36, 25 * 36)  # in kWs/km

    async def run(self):
        while True:
            await self.drive()
            await self.sleep()
            if self.soc < self.capacity*0.5:
                await self.charge()

    async def drive(self):
        print("start driving...")
        distance = random.randint(1, 10)  # distance to drive in km
        # duration in seconds when driving the distance witrh 50 km/h
        duration = int((distance / 50) * 3600)
        energy_consumed = distance * self.consumption
        self.soc -= energy_consumed
        if not self.soc > 0:
            print("The car has died...")
        await asyncio.sleep(duration/TIMELAPSE)
        print(f"drove for {duration} seconds.")

    async def sleep(self):
        print("sleeping...")
        # sleep between a minute and an hour
        duration = random.randint(60, 3600)
        await asyncio.sleep(duration/TIMELAPSE)
        print("slept ")

    async def charge(self):
        print("want to charge now")
        await self.chargepoint.charge(self)
        print(self.soc)
