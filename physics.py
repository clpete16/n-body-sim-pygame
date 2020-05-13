import math as m


class Obj:

    def __init__(self,
                 mass=1,
                 radius=1,
                 position=[0, 0, 0],
                 velocity=[0, 0, 0],
                 G=6.67408 * 10**-11,
                 color = [200, 200, 200],
                 name = "unnammed",
                 actOnOthers = True
                 ):
        self.mass = mass
        self.radius = radius
        self.position = position
        self.velocity = velocity
        self.G = G
        self.color = color
        self.name = name
        self.actOnOthers = actOnOthers
        
    def update_velocity(self, objects, timestep):
        # V = V0 + A*t
        # A = GM/r^2
        for B in objects:
            if B != self and B.actOnOthers:
                A = self
                dx = A.position[0] - B.position[0]
                dy = A.position[1] - B.position[1]
                dz = A.position[2] - B.position[2]
                distance = m.sqrt(dx*dx + dy*dy + dz*dz)
                direction = [-dx / distance, -dy / distance, -dz / distance]
                delta = vector_multiply(
                    direction, (self.G * B.mass / distance / distance * timestep))
                self.velocity = vector_add(self.velocity, delta)

    def update_position(self, timestep):
        # X = X0 + V*t
        delta = vector_multiply(self.velocity, timestep)
        self.position = vector_add(self.position, delta)

    def shift_by_angle(self, angle):
        angle = angle * m.pi / 180
        self.position = [
            self.position[0] * m.cos(angle),
            self.position[0] * m.sin(angle),
            self.position[2]
        ]
        self.velocity = [
            self.velocity[1] * m.cos(angle + m.pi/2),
            self.velocity[1] * m.sin(angle + m.pi/2),
            self.velocity[2]
        ]


def vector_multiply(vector, scalar):
    return [
        vector[0] * scalar,
        vector[1] * scalar,
        vector[2] * scalar
    ]


def vector_add(A, B):
    return [
        A[0] + B[0],
        A[1] + B[1],
        A[2] + B[2]
    ]
