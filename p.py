import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def calculate_precise_daylight(latitude, day_of_year):
    """
    High-precision daylight calculation based on NOAA solar algorithms.
    Accounts for atmospheric refraction (-0.833 degrees).
    """
    # 1. Fractional year in radians
    gamma = (2 * np.pi / 365) * (day_of_year - 1)
    
    # 2. Solar declination angle (radians) - Precise NOAA Formula
    decl = 0.006918 - 0.399912 * np.cos(gamma) + 0.070257 * np.sin(gamma) - \
           0.006758 * np.cos(2 * gamma) + 0.000907 * np.sin(2 * gamma) - \
           0.002697 * np.cos(3 * gamma) + 0.00148 * np.sin(3 * gamma)
    
    # 3. Hour angle for sunrise/sunset
    # Standard zenith for sunrise/sunset is 90.833 degrees (includes refraction)
    zenith_rad = np.radians(90.833)
    lat_rad = np.radians(latitude)
    
    cos_ha = (np.cos(zenith_rad) / (np.cos(lat_rad) * np.cos(decl))) - (np.tan(lat_rad) * np.tan(decl))
    cos_ha = np.clip(cos_ha, -1, 1) # Prevents errors at poles
    
    ha_deg = np.degrees(np.arccos(cos_ha))
    
    # Daylight hours = (2 * hour_angle) / 15 degrees per hour
    return (2 * ha_deg) / 15

# 1. Setup Data for 2026
days = np.arange(1, 366)
dates = pd.to_datetime(days - 1, unit='D', origin='2026-01-01')

seattle_lat = 47.6062
saigon_lat = 10.8231

seattle_hours = np.array([calculate_precise_daylight(seattle_lat, d) for d in days])
saigon_hours = np.array([calculate_precise_daylight(saigon_lat, d) for d in days])

# 2. Create Plot
plt.style.use('fivethirtyeight')
fig, ax = plt.subplots(figsize=(12, 8))

# Plotting area charts
ax.fill_between(dates, seattle_hours, color="skyblue", alpha=0.5, label="Seattle (47.6°N)")
ax.plot(dates, seattle_hours, color="steelblue", lw=3)

ax.fill_between(dates, saigon_hours, color="orange", alpha=0.4, label="Saigon (10.8°N) - Sài Gòn")
ax.plot(dates, saigon_hours, color="darkorange", lw=3)

# 3. Bilingual Titles and Labels
title_str = "Seattle vs Saigon daylight comparison by Mycole\nSo sánh thời gian ban ngày giữa Seattle và Sài Gòn"
ax.set_title(title_str, fontsize=16, pad=25)
ax.set_ylabel("Hours of Daylight / Số giờ ban ngày", fontsize=12)
ax.set_xlabel("Month / Tháng", fontsize=12)
ax.set_ylim(0, 19)
ax.legend(loc="upper right", fontsize=10)

# 4. Annotations for the "Same Hours" points (Equinoxes)
# March 20 is Day 79 (index 78) and Sept 22 is Day 265 (index 264)
equinox_indices = [78, 264]
equinox_dates = ["20/03", "22/09"]
label_intersection = "Equal Daylight\nBằng nhau"

for i, idx in enumerate(equinox_indices):
    ax.annotate(f"{label_intersection}\n({equinox_dates[i]})", 
                xy=(dates[idx], seattle_hours[idx]), 
                xytext=(dates[idx], seattle_hours[idx] - 4.5),
                arrowprops=dict(facecolor='black', shrink=0.08, width=1.5, headwidth=8),
                ha='center', fontsize=10, fontweight='bold', color='black')

# Summer Solstice (June 21 is index 171)
ax.annotate('Summer Solstice\nHạ chí (21/06)', 
            xy=(pd.Timestamp('2026-06-21'), seattle_hours[171]), 
            xytext=(pd.Timestamp('2026-08-15'), 17.5),
            arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8),
            ha='center', fontsize=10)

plt.tight_layout()
plt.savefig("daylight_precise_2026.png", dpi=300)