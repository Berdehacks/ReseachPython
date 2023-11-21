import numpy as np
import pyvista
import socket
import struct

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 1733))
done = False

number_of_lines = 300
list_of_line_scans = [[] for _ in range(number_of_lines)]
global_counter = 0
should_start_drawing_image = False

while not done:
    data = client_socket.recv(4096)
    print(data)

    if global_counter >= number_of_lines:
        should_start_drawing_image = True
        global_counter = 0

    xs = []
    ys = []
    zs = []
    intensities = []
    rs = []
    thetas = []
    phis = []

    for i in range(0, len(data), 16):
        x_float = struct.unpack('f', data[i : i+4])
        xs.append(x_float)

        y_float = struct.unpack('f', data[i+4 : i+8])
        ys.append(y_float)

        z_float = struct.unpack('f', data[i+8 : i+12])
        zs.append(z_float)

        intensity_float = struct.unpack('f', data[i+12 : i+16])
        intensities.append(intensity_float[0])

        # spherical_coords = cartesian_to_spherical(np.array([x_float, y_float, z_float]))
        # rs.append(spherical_coords[0])
        # thetas.append(spherical_coords[1])
        # phis.append(spherical_coords[2])

    print(len(xs), len(ys), len(zs))
    point_cloud = np.zeros((len(xs), 3))

    point_cloud[:, 0] = xs[:]
    print(point_cloud)
    # point_cloud[:, 1] = ys
    # point_cloud[:, 2] = zs

    print(point_cloud.shape)
    pdata = pyvista.PolyData(point_cloud)
    pdata['orig_sphere'] = np.arange(1000)

    sphere = pyvista.Sphere(radius=0.02, phi_resolution=10, theta_resolution=10)
    pc = pdata.glyph(scale=False, geom=sphere, orient=False)
    pc.plot(cmap='Reds')
