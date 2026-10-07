"""Understanding Guidance & Path Tracking Using an Autonomous Boat 🚤
This task is designed to help understand the intuition behind guidance and feedback control without focusing on heavy coding.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Polygon
from IPython.display import HTML, display
from ipywidgets import interact, FloatSlider

def create_boat(x, y, theta, scale=0.8):
    boat = np.array([
        [1.5, 0],
        [-1, 0.7],
        [-0.5, 0],
        [-1, -0.7]
    ]) * scale

    R = np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta),  np.cos(theta)]
    ])

    rotated_boat = boat @ R.T
    rotated_boat[:,0] += x
    rotated_boat[:,1] += y

    return rotated_boat

def boat_guidance(kp=1.0, kd=0.0, current_x=0.3, current_y=0.3):
    dt = 0.2
    T = 40
    t = np.arange(0, T, dt)

    path_x = t
    path_y = 8*np.sin(0.2*t)

    x, y = -5, -10
    vx, vy = 0, 0
    traj_x = []
    traj_y = []
    headings = []

    for i in range(len(t)):
        dx = path_x[i] - x
        dy = path_y[i] - y

        ax = kp*dx - kd*vx + current_x
        ay = kp*dy - kd*vy + current_y

        vx += ax*dt
        vy += ay*dt
        x += vx*dt
        y += vy*dt

        traj_x.append(x)
        traj_y.append(y)
        headings.append(np.arctan2(vy, vx))

    plt.figure(figsize=(10,6))
    plt.plot(path_x, path_y, '--', linewidth=2, label='Desired Path')
    plt.plot(traj_x, traj_y, linewidth=3, label='Boat Trajectory')
    plt.scatter(traj_x[0], traj_y[0], s=100, label='Start')
    plt.scatter(traj_x[-1], traj_y[-1], s=100, label='End')

    boat_shape = create_boat(traj_x[-1], traj_y[-1], headings[-1])
    boat_patch = Polygon(boat_shape, closed=True)
    plt.gca().add_patch(boat_patch)

    plt.quiver(traj_x[-1], traj_y[-1], current_x, current_y, scale=5)
    plt.title(f'Boat Guidance | Gain={kp} | Damping={kd}')
    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.grid(True)
    plt.legend()
    plt.xlim(min(path_x)-5, max(path_x)+5)
    plt.ylim(min(path_y)-15, max(path_y)+15)
    plt.show()

interact(
    boat_guidance,
    kp=FloatSlider(value=1.0, min=0.1, max=2.0, step=0.1, description='Gain'),
    kd=FloatSlider(value=0.0, min=0.0, max=3.0, step=0.1, description='Damping'),
    current_x=FloatSlider(value=0.3, min=-1.0, max=1.0, step=0.1, description='Current X'),
    current_y=FloatSlider(value=0.3, min=-1.0, max=1.0, step=0.1, description='Current Y')
)

def animate_boat(kp=1.0, kd=0.0, current_x=0.3, current_y=0.3):
    dt = 0.2
    T = 35
    t = np.arange(0, T, dt)

    path_x = t
    path_y = 8*np.sin(0.2*t)

    x, y = -5, -10
    vx, vy = 0, 0
    traj_x = []
    traj_y = []
    headings = []

    for i in range(len(t)):
        dx = path_x[i] - x
        dy = path_y[i] - y

        ax = kp*dx - kd*vx + current_x
        ay = kp*dy - kd*vy + current_y

        vx += ax*dt
        vy += ay*dt
        x += vx*dt
        y += vy*dt

        traj_x.append(x)
        traj_y.append(y)
        headings.append(np.arctan2(vy, vx))

    fig, ax = plt.subplots(figsize=(10,6))
    ax.set_xlim(min(path_x)-5, max(path_x)+5)
    ax.set_ylim(min(path_y)-15, max(path_y)+15)
    ax.set_title('Animated Boat Guidance')
    ax.set_xlabel('X Position')
    ax.set_ylabel('Y Position')
    ax.grid(True)

    ax.plot(path_x, path_y, '--', linewidth=2, label='Desired Path')
    traj_line, = ax.plot([], [], linewidth=3, label='Boat Trajectory')
    
    initial_boat = create_boat(traj_x[0], traj_y[0], headings[0])
    boat_patch = Polygon(initial_boat, closed=True)
    ax.add_patch(boat_patch)

    X, Y = np.meshgrid(
        np.linspace(min(path_x)-5, max(path_x)+5, 15),
        np.linspace(min(path_y)-15, max(path_y)+15, 10)
    )

    U = current_x*np.ones_like(X)
    V = current_y*np.ones_like(Y)
    water = ax.quiver(X, Y, U, V, alpha=0.6)
    ax.legend()

    def update(frame):
        traj_line.set_data(traj_x[:frame], traj_y[:frame])
        new_boat = create_boat(traj_x[frame], traj_y[frame], headings[frame])
        boat_patch.set_xy(new_boat)
        return traj_line, boat_patch

    anim = FuncAnimation(fig, update, frames=len(t), interval=60, blit=False)
    plt.close(fig)
    return HTML(anim.to_html5_video())

animate_boat(kp=1.2, kd=0.0, current_x=0.12, current_y=0.12)
