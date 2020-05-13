import physics
import time
import render
from random import randint
import math as m

"""
TO DO:
Add debugging orbit-line
"""


class Settings:

    def __init__(self,
                 fps=30,
                 timestep=3600 * 24,  # 1 day per second
                 timescale=365.25 * 3600 * 24,  # 1 year (for labels)
                 maxMultiplier=50,
                 minMultiplier=50,
                 word="years",
                 center=False,
                 centerNum=0,
                 distScale=1,
                 showLabels = True
                 ):
        self.width = 1600
        self.height = 900
        self.FPS = fps

        self.choosing = True        # Choosing which set of objects
        self.active = False         # Running the sim
        self.restart = False        # Restart the sim upon exit

        self.timestep = timestep / fps
        self.timescaleWord = " " + word
        self.timescale = timescale
        self.maxTimestep = maxMultiplier * timescale
        self.minTimestep = timescale / minMultiplier
        self.centerOnObject = center
        self.centerObjectNumber = centerNum
        self.distScale = distScale
        self.showLabels = showLabels


def make_solar_system(doRoids=False, numRoids=50):
    objects = []

    settings = Settings(
        distScale=1.496 * 10**11,
        center=True)

    sun = physics.Obj(mass=1.989 * 10**30,
                      color=[200, 200, 50],
                      radius=5,
                      name="Sol")
    objects.append(sun)

    mercury = physics.Obj(mass=0.33 * 10**24,
                          position=[46*10**9, 0, 0],
                          velocity=[0, 58980, 0],
                          color=[200, 150, 100],
                          radius=2,
                          name="Mercury")
    mercury.shift_by_angle(77.45645)
    objects.append(mercury)

    venus = physics.Obj(mass=4.87 * 10**24,
                        position=[107.48*10**9, 0, 0],
                        velocity=[0, 35260, 0],
                        color=[150, 75, 75],
                        radius=6,
                        name="Venus")
    venus.shift_by_angle(131.53298)
    objects.append(venus)

    earth = physics.Obj(mass=5.9724 * 10**24,
                        position=[147.09*10**9, 0, 0],
                        velocity=[0, 30290, 0],
                        color=[0, 100, 40],
                        radius=6,
                        name="Earth")
    earth.shift_by_angle(102.94719)
    objects.append(earth)

    mars = physics.Obj(mass=0.642 * 10**24,
                       position=[206.62*10**9, 0, 0],
                       velocity=[0, 26500, 0],
                       color=[200, 100, 50],
                       radius=4,
                       name="Mars")
    mars.shift_by_angle(336.04084)
    objects.append(mars)

    jupiter = physics.Obj(mass=1898 * 10**24,
                          position=[740.52*10**9, 0, 0],
                          velocity=[0, 13720, 0],
                          color=[100, 50, 35],
                          radius=71,
                          name="Jupiter")
    jupiter.shift_by_angle(14.75385)
    objects.append(jupiter)

    saturn = physics.Obj(mass=568 * 10**24,
                         position=[1352.55*10**9, 0, 0],
                         velocity=[0, 10180, 0],
                         color=[200, 100, 70],
                         radius=60,
                         name="Saturn")
    saturn.shift_by_angle(92.43194)
    objects.append(saturn)

    uranus = physics.Obj(mass=86.8 * 10**24,
                         position=[2741.3*10**9, 0, 0],
                         velocity=[0, 7110, 0],
                         color=[200, 200, 255],
                         radius=25,
                         name="Uranus")
    uranus.shift_by_angle(170.96424)                         
    objects.append(uranus)

    neptune = physics.Obj(mass=102 * 10**24,
                          position=[4444.45*10**9, 0, 0],
                          velocity=[0, 5500, 0],
                          color=[100, 100, 150],
                          radius=25,
                          name="Neptune")
    neptune.shift_by_angle(44.97135)
    objects.append(neptune)

    pluto = physics.Obj(mass=0.0146 * 10**24,
                        position=[4436.82*10**9, 0, 0],
                        velocity=[0, 6100, 0],
                        color=[220, 220, 220],
                        radius=1,
                        name="Pluto")
    pluto.shift_by_angle(224.06676)
    objects.append(pluto)

    if doRoids:
        for _ in range(numRoids):
            distanceToSun = randint(3000000, 11000000) * 10**5
            roid = physics.Obj(
                position = [distanceToSun, 0, 0],
                velocity = [0, m.sqrt(1.327*10**20 / distanceToSun), 0],
                actOnOthers=False
            )
            angle = randint(0, 359)
            roid.shift_by_angle(angle)
            objects.append(roid)

    return objects, settings


def make_earth_moon_system():
    objects = []

    settings = Settings(
        timescale=3600*24,
        word="days",
        distScale=10**8,
        center=True,
        maxMultiplier=28)

    earth = physics.Obj(mass=5.9724 * 10**24,
                        color=[0, 100, 40],
                        radius=20,
                        name="Earth")
    objects.append(earth)

    moon = physics.Obj(mass=0.07346 * 10**24,
                       position=[0.3633 * 10**9, 0.0, 0.0],
                       velocity=[0.0, 1082, 0.0],
                       radius=5,
                       name="Moon")
    objects.append(moon)

    moon2 = physics.Obj(mass=0.2 * 10**24,
                        position=[-10**9, 0, 0],
                        velocity=[0, -350, 0],
                        color=[100, 100, 100],
                        radius=8,
                        name="Moon?")
    # objects.append(moon2)
    return objects, settings


def make_figure_eight_system():
    objects = []

    # Chenciner & Montgomery
    settings = Settings(
        timestep = 1,
        distScale = 0.1,
        timescale = 1,
        word = "seconds",
        maxMultiplier=120,
        minMultiplier=10
    )

    a = physics.Obj(position=[-0.97000436, 0.24308753, 0],
                    velocity=[0.4662036850, 0.4323657400, 0],
                    color=[200, 0, 0],
                    radius=20,
                    G=1,
                    name="Red")
    objects.append(a)

    b = physics.Obj(velocity=[-0.93240737, -0.86473146, 0],
                    color=[0, 200, 0],
                    radius=20,
                    G=1,
                    name="Green")
    objects.append(b)

    c = physics.Obj(position=[0.97000436, -0.24308753, 0],
                    velocity=[0.4662036850, 0.4323657400, 0],
                    color=[0, 0, 200],
                    radius=20,
                    G=1,
                    name="Blue")
    objects.append(c)
    return objects, settings


def make_asteroid_belt_system(numRoids):
    objects = []

    settings = Settings(
        distScale=1.496 * 10**11,
        timescale=365.25 * 24 * 3600,
        center=True,
        showLabels=False)
    
    sun = physics.Obj(mass=1.989 * 10**30,
                      color=[200, 200, 50],
                      radius=5,
                      name="Sol")
    objects.append(sun)

    jupiter = physics.Obj(mass=1898 * 10**24,
                          position=[740.52*10**9, 0, 0],
                          velocity=[0, 13720, 0],
                          color=[100, 50, 35],
                          radius=20,
                          name="Jupiter")
    objects.append(jupiter)

    saturn = physics.Obj(mass=568 * 10**24,
                         position=[1352.55*10**9, 0, 0],
                         velocity=[0, 10180, 0],
                         color=[200, 100, 70],
                         radius=15,
                         name="Saturn")
    objects.append(saturn)

    for _ in range(numRoids):
        distanceToSun = randint(652450000, 897150000*1.5) * 10**3
        roid = physics.Obj(
            position = [distanceToSun, 0, 0],
            velocity = [0, m.sqrt(1.327*10**20 / distanceToSun), 0],
            actOnOthers=False
        )
        angle = randint(0, 359)
        roid.shift_by_angle(angle)
        objects.append(roid)

    return objects, settings


def sim_no_display(objects, settings):
    count = 0
    maxCount = 100000

    settings.timestep *= settings.FPS

    while count < maxCount:
        for obj in objects:
            obj.update_velocity(objects, settings.timestep)

        for obj in objects:
            obj.update_position(settings.timestep)

        if count % 1000 == 0:
            print('Count: ' + str(count))
        count += 1

    sim_display(objects, settings)


def sim_display(objects, settings):
    gameWindow = render.GameWindow(settings)

    stepsPerFrame = 1
    timeSinceEpoch = 0
    framecount = 0

    while settings.active:

        gameWindow.delay_until_next_frame(settings.FPS)
        gameWindow.process_inputs(settings)
        gameWindow.reset_frame()

        # Physics
        tic = time.perf_counter()
        if stepsPerFrame <= 0:
            stepsPerFrame = 1
        ts = settings.timestep / stepsPerFrame

        for __ in range(stepsPerFrame):
            for obj in objects:
                obj.update_velocity(objects, ts)

            for obj in objects:
                obj.update_position(ts)

        avg = (time.perf_counter() - tic) / stepsPerFrame
        stepsPerFrame = round((1 / settings.FPS - 0.003) / avg)

        if framecount == settings.FPS:
            print(stepsPerFrame*settings.FPS)
            framecount = 0

        # Draw the next frame
        gameWindow.draw_objects(objects, settings)
        gameWindow.draw_static_labels()
        gameWindow.draw_dynamic_labels(settings, timeSinceEpoch, objects)
        gameWindow.update_frame()

        timeSinceEpoch += settings.timestep
        framecount += 1


def choose_system(settings):

    gameWindow = render.GameWindow(settings)
    gameWindow.make_choice_screen()

    while settings.choosing:
        gameWindow.delay_until_next_frame(settings.FPS)
        gameWindow.process_inputs(settings)
        gameWindow.reset_frame()
        gameWindow.draw_buttons()

        for i in range(len(gameWindow.buttons)):
            if gameWindow.buttons[i].isOver():
                choice = i + 1
                settings.choosing = False

        gameWindow.update_frame()

    return choice


def main():
    settings = Settings()

    choice = choose_system(settings)

    if choice == 1:
        objects, settings = make_solar_system()
    elif choice == 2:
        objects, settings = make_earth_moon_system()
    elif choice == 3:
        objects, settings = make_figure_eight_system()
    elif choice == 4:
        objects, settings = make_asteroid_belt_system(500)

    settings.active = True
    sim_display(objects, settings)

    if settings.restart:
        main()


if __name__ == "__main__":
    main()
