import random
from colorama import Fore

DEFAULT_SPEED = 2
DETECTION_RANGE = 3
SPEED_VARIATION = [-2, -1, 0]
ROAD_LENGTH = 400
DEFAULT_SPACING = 5


class Car:

    def __init__(self, id):
        self.speed = DEFAULT_SPEED
        self.detection_range = DETECTION_RANGE + random.choices([-1, 0, 1], [25, 50, 25], k=1)[0]
        self.id = id
        self.behind_a_car = False
        self.position = id

    def increment(self):
        if not self.behind_a_car and self.speed == DEFAULT_SPEED:
            self.speed = self.speed + random.choices(population=SPEED_VARIATION, weights=[1, 4, 95], k=1)[0]
        elif not self.behind_a_car and self.speed < DEFAULT_SPEED:
            self.speed += random.choices(population=[0, 1], weights=[80, 20], k=1)[0]
        return self.speed

    def __str__(self):
        string = '\U0001F697'
        return string

    def color(self):
        if self.speed == DEFAULT_SPEED - 1:
            return Fore.LIGHTYELLOW_EX
        if self.speed == DEFAULT_SPEED:
            return Fore.GREEN
        if self.speed == DEFAULT_SPEED - 2:
            return Fore.RED
        if self.speed <= DEFAULT_SPEED - 3:
            return Fore.BLACK

class Road:
    state_of_road = {}
    cars = []

    def increment(self):
        for item in self.cars:
            item.increment()
            position = item.position
            self.state_of_road[position] = []
            if not position >= ROAD_LENGTH - item.detection_range - 1:
                marker = False
                for y in range(position, position+1+item.detection_range):
                    if len(self.state_of_road[y]) == 1:
                        marker = True
                        item.speed = self.state_of_road[y][0].speed
                item.behind_a_car = marker
                position += item.speed
                item.position = position
                if not item.position > len(self.state_of_road):
                    self.state_of_road[position].append(item)

    def create(self, length):
        for i in range(0, length+1):
            self.state_of_road[i] = []
            if i % DEFAULT_SPACING == 0:
                car = Car(i)
                self.state_of_road[i].append(car)
                self.cars.insert(0, car)

    def __str__(self):
        string = ''
        for key in self.state_of_road:
            if len(self.state_of_road[key]) == 1:
                string += self.state_of_road[key][0].color() + str(self.state_of_road[key][0])
            else:
                string += Fore.RESET + '_'
        return string


def boot():
    road = Road()
    road.create(ROAD_LENGTH)
    for i in range(0, 150):
        print(str(road))
        road.increment()


if __name__ == '__main__':
    boot()

