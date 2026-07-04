# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""Great-circle geometry on a lat/long grid and the error of flat approximations.

Left: the great-circle path between two cities curves across an equirectangular
(plate carree) grid, unlike the straight lat/long segment. Right: the relative
error of the naive Euclidean-in-degrees and equirectangular approximations to the
true haversine distance, as a function of angular separation at latitude 45 deg.
"""

import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, MUTED

apply_style()

R = 6371.0  # mean Earth radius, km


def haversine(lat1, lon1, lat2, lon2):
    p1, p2 = np.radians(lat1), np.radians(lat2)
    dphi = np.radians(lat2 - lat1)
    dlam = np.radians(lon2 - lon1)
    a = np.sin(dphi / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(dlam / 2) ** 2
    return R * 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))


def great_circle_path(lat1, lon1, lat2, lon2, n=100):
    """Slerp between two surface points; return arrays of lat/long along the arc."""
    p1 = np.radians([lat1, lon1])
    p2 = np.radians([lat2, lon2])

    def to_xyz(lat, lon):
        return np.array([np.cos(lat) * np.cos(lon),
                         np.cos(lat) * np.sin(lon),
                         np.sin(lat)])

    v1, v2 = to_xyz(*p1), to_xyz(*p2)
    omega = np.arccos(np.clip(v1 @ v2, -1, 1))
    t = np.linspace(0, 1, n)
    v = (np.sin((1 - t)[:, None] * omega) * v1 + np.sin(t[:, None] * omega) * v2) / np.sin(omega)
    lat = np.degrees(np.arcsin(v[:, 2]))
    lon = np.degrees(np.arctan2(v[:, 1], v[:, 0]))
    return lat, lon


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2))

# --- Left: great-circle path New York -> London on a lat/long grid ---
ny = (40.7128, -74.0060)
lon_ = (51.5074, -0.1278)
gc_lat, gc_lon = great_circle_path(*ny, *lon_)

ax1.plot([ny[1], lon_[1]], [ny[0], lon_[0]], "--", color=MUTED,
         label="straight lat/long segment")
ax1.plot(gc_lon, gc_lat, color=PALETTE[1], lw=2.2, label="great-circle path")
ax1.scatter([ny[1], lon_[1]], [ny[0], lon_[0]], color=PALETTE[0], zorder=5)
ax1.annotate("New York", ny[::-1], textcoords="offset points", xytext=(6, -12))
ax1.annotate("London", lon_[::-1], textcoords="offset points", xytext=(-30, 8))
ax1.set_xlabel("Longitude (deg)")
ax1.set_ylabel("Latitude (deg)")
ax1.set_title("Great circle vs. straight lat/long line")
ax1.legend(loc="lower right", fontsize=9)

# --- Right: relative error of flat approximations vs separation at lat 45 ---
lat0 = 45.0
seps = np.linspace(1.0, 2000.0, 200)  # true distance, km
# place a second point due east so the longitude (cos) effect dominates
dlam = np.degrees(seps / (R * np.cos(np.radians(lat0))))
true = haversine(lat0, 0.0, lat0, dlam)

deg_km = R * np.pi / 180.0  # km per degree of arc
naive = deg_km * np.hypot(0.0, dlam)                     # Euclidean in raw degrees
equirect = deg_km * np.hypot(0.0, np.cos(np.radians(lat0)) * dlam)  # equirectangular

ax2.plot(true, 100 * (naive - true) / true, color=PALETTE[0],
         label="Euclidean degrees")
ax2.plot(true, 100 * (equirect - true) / true, color=PALETTE[2],
         label="equirectangular")
ax2.axhline(0, color=MUTED, lw=0.8)
ax2.set_xlabel("True great-circle distance (km)")
ax2.set_ylabel("Relative error (%)")
ax2.set_title("Approximation error at 45 deg latitude")
ax2.legend(loc="center right", fontsize=9)

save(fig, "assets/figures/distance-measures.svg")
