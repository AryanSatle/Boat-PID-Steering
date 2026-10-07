import csv
import matplotlib.pyplot as plt

time, set_x, set_y, pos_x, pos_y, ctrl_x, ctrl_y = [], [], [], [], [], [], []

with open('boat_pd_output.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        time.append(int(row['Time']))
        set_x.append(int(row['SetX']))
        set_y.append(int(row['SetY']))
        pos_x.append(int(row['PosX']))
        pos_y.append(int(row['PosY']))
        ctrl_x.append(int(row['ControlX']))
        ctrl_y.append(int(row['ControlY']))

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))

ax1.plot(set_x, set_y, 'r--', linewidth=2, label='Desired Path')
ax1.plot(pos_x, pos_y, 'b-', linewidth=2, label='Boat Trajectory')
ax1.scatter([pos_x[0]], [pos_y[0]], color='green', s=100, label='Start')
ax1.scatter([pos_x[-1]], [pos_y[-1]], color='purple', s=100, label='End')
ax1.set_title('2D Boat Path Tracking')
ax1.set_xlabel('X Position')
ax1.set_ylabel('Y Position')
ax1.grid(True, linestyle=':', alpha=0.7)
ax1.legend()

ax2.plot(time, ctrl_x, 'm-', label='Control X (Steering/Thrust X)')
ax2.plot(time, ctrl_y, 'c-', label='Control Y (Steering/Thrust Y)')
ax2.axvspan(120, 200, color='gray', alpha=0.2, label='Current Shift Disturbance')
ax2.set_title('Controller Output over Time')
ax2.set_xlabel('Time (Clock Cycles)')
ax2.set_ylabel('Control Signal')
ax2.grid(True, linestyle=':', alpha=0.7)
ax2.legend()

plt.tight_layout()
plt.savefig('boat_verification_plots.png')
plt.show()
