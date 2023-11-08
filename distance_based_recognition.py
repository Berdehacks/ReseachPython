import numpy as np
import matplotlib.pyplot as plt

# generate random positions
grid_size = 100
number_of_beacons = 10
distance_rounding = 2

# generate beacons
beacons_positions: np.ndarray = np.random.rand(number_of_beacons, 2) * grid_size

beacons_distances_map: dict[np.floating, tuple[np.ndarray, np.ndarray]] = {}

# compare distance to every other beacon and save it
for beacon_a_index in range(len(beacons_positions)):
    for beacon_b_index in range(beacon_a_index + 1, len(beacons_positions)):
        beacon_a = beacons_positions[beacon_a_index]
        beacon_b = beacons_positions[beacon_b_index]

        distance: np.floating = np.linalg.norm(beacon_a - beacon_b)
        usable_distance = round(distance, distance_rounding)

        # check if rounding distance has already been used
        if usable_distance in beacons_distances_map:
            raise Exception(f"The distances between beacons {beacons_distances_map[usable_distance]} and {beacon_a, beacon_b} seem to have the same distance at {usable_distance}")

        beacons_distances_map[usable_distance] = (beacon_a, beacon_b)

# run test to check if we did everything right
# we won't know which beacons we've found
beacons_found = np.random.choice(number_of_beacons, 2, replace=False)

print(beacons_distances_map)

# this will be the input data
found_distance = round(np.linalg.norm(beacons_positions[beacons_found[0]] - beacons_positions[beacons_found[1]]), distance_rounding)
print(f"found beacons at positions {beacons_distances_map[found_distance]} with distance {found_distance}")

plt.plot(beacons_positions[:, 0], beacons_positions[:, 1], "-o")
plt.show()
