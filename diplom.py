from node import Node
from particle import Particle
from vector2d import Vector2d
from bh_tree import BHtree
from profiler import Profiler
import random
import io_xyz
import math
import forces
import constants
import plotting
import os

# import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib



def make_net(n_particles=int(10e6)):
    particles = []
    n_rows = int(math.sqrt(n_particles))
    h = constants.box_size // n_rows
    for i in range(n_particles):
        particles.append(Particle(r=Vector2d(i % n_rows * h, i // n_rows * h), v=Vector2d()))
        # print(particles[-1].r)

    return particles, h


def make_hex(k=10, l=10):
    # k количество рядов до середины
    # l количество в крайнем ряду
    particles = []
    for i in range(k):
        for j in range(i + l):
            particles.append(
                Particle(r=Vector2d(constants.a * i * math.sqrt(3) / 2,
                                    constants.a * j - constants.a * 0.5 * i),
                         v=Vector2d(), name=len(particles)))
    for i in range(k, 2 * k - 1):
        for j in range(l + k - 2 - (i - k)):
            particles.append(Particle(r=Vector2d(constants.a * i * math.sqrt(3) / 2,
                                                 constants.a * j + constants.a * 0.5 * (i - 2 * k + 2)),
                                      v=Vector2d(), name=len(particles)))
    return particles


box_size = constants.box_size

particles = make_hex(constants.k, constants.l)
print(len(particles))

fig, ax1 = plt.subplots(figsize=(4, 4))
x = [particle.r.x for particle in particles]
y = [particle.r.y for particle in particles]
ax1.scatter(x=x, y=y, marker='o', c='r', edgecolor='b')
ax1.set_title('Scatter: $x$ versus $y$')
ax1.set_xlabel('$x$')
ax1.set_ylabel('$y$')
plt.show()

# for particle in particles:
#     particle.v = Vector2d(10*random.random(), 10*random.random())

save_path = os.path.dirname(os.path.realpath(__file__)) + '/test'
if not os.path.exists(save_path):
    os.makedirs(save_path)


for step in range(constants.steps_number):
    print(step)

    with open(save_path + '/results_' + str(step) + '.xyz', 'w') as outfile:
        outfile.write(str(len(particles)) + '\n\n')
        for i, particle in enumerate(particles):
            outfile.write(str(particle.r) + ' ' +
                          str(particle.color[0]) + ' ' +
                          str(particle.color[1]) + ' ' +
                          str(particle.color[2]) + ' ' + '\n')

    n1 = Node([-box_size / 2, -box_size / 2, box_size / 2, box_size / 2], node_type=2)
    bh = BHtree(n1)

    for particle in particles:
        bh.insert_particle(particle, bh.root)

    # if step == 0:
    #     plotting.plot_main(particles, bh)

    for particle in particles:
        particle.force = bh.calculate_force(particle)

    for particle in particles:
        particle.v += particle.force * constants.dt
        particle.r += particle.v * constants.dt

    del bh
