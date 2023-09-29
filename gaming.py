import numpy as np

A = np.array([1294810, -100, -2100830])
B = np.array([3, 3, 12900])
C = np.array([-2, -3, -10])

CB = C - B
r2 = np.linalg.norm(CB)
theta2 = np.arctan2(CB[1], CB[0])
phi2 = np.arccos(CB[2] / r2)

CA = C - A
r1 = np.linalg.norm(CA)
theta1 = np.arctan2(CA[1], CA[0])
phi1 = np.arccos(CA[2] / r1)

Ax, Ay, Az = (A[0], A[1], A[2])
Bx, By, Bz = (B[0], B[1], B[2])

print("A: ", r1, np.rad2deg(theta1), np.rad2deg(phi1))
print("B: ", r2, np.rad2deg(theta2), np.rad2deg(phi2))

up = Ax + np.tan(phi1) * np.cos(theta1) * (Bz - Az) - Bx
down = np.sin(phi2) * np.cos(theta2) - np.tan(phi1) * np.cos(phi2) * np.cos(theta1)

new_r2 = up / down

B_e = np.array([
    new_r2 * np.sin(phi2) * np.cos(theta2),
    new_r2 * np.sin(phi2) * np.sin(theta2),
    new_r2 * np.cos(phi2)
])

print(B + B_e)

