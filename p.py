import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def calculate_daylight_hours(latitude, day_of_year):
    """
    Standard formula for daylight duration:
    Uses the declination of the sun and the latitude to find the hour angle.
    """
    declination = 23.45 * np.sin(np.radians((360 / 365) * (day_of_year - 80)))
    lat_rad = np.radians(latitude)
    decl_rad = np.radians(declination)
    cos_h = -np.tan(lat_rad) * np.tan(decl_rad)
    cos_h = np.clip(cos_h, -1, 1)
    hour_angle = np.degrees(np.arccos(cos_h))
    return (2 / 15) * hour_angle

# 1. Setup Data
days = np.arange(1, 366)
dates = pd.to_datetime(days - 1, unit='D', origin='2026-01-01')

seattle_lat = 47.6062
saigon_lat = 10.8231

seattle_hours = np.array([calculate_daylight_hours(seattle_lat, d) for d in days])
saigon_hours = np.array([calculate_daylight_hours(saigon_lat, d) for d in days])

# Find intersection points where daylight is equal
diff = np.abs(seattle_hours - saigon_hours)
idx1 = np.argmin(diff[0:150])           # Spring Equinox search
idx2 = np.argmin(diff[150:365]) + 150   # Autumn Equinox search

# 2. Create Plot
plt.style.use('fivethirtyeight')
fig, ax = plt.subplots(figsize=(12, 8))

# Plotting the area charts
ax.fill_between(dates, seattle_hours, color="skyblue", alpha=0.5, 
                label="Seattle (47.6°N) - ")
ax.plot(dates, seattle_hours, color="steelblue", lw=3)

ax.fill_between(dates, saigon_hours, color="orange", alpha=0.4, 
                label="Saigon (10.8°N) - Sài Gòn")
ax.plot(dates, saigon_hours, color="darkorange", lw=3)

# 3. Bilingual Titles and Labels
title_str = "Seattle vs Saigon daylight comparison by Mycole\nSo sánh thời gian ban ngày giữa Seattle và Sài Gòn"
ax.set_title(title_str, fontsize=16, pad=25)

ax.set_ylabel("Hours of Daylight / Số giờ ban ngày", fontsize=12)
ax.set_xlabel("Month / Tháng", fontsize=12)
ax.set_ylim(0, 19)
ax.legend(loc="upper right", fontsize=10)

# 4. Add Annotations for the "Same Hours" points (Equinoxes)
label_intersection = "Equal Daylight\nBằng nhau"
# 4. Add Annotations for the "Same Hours" points (Equinoxes)
# Using calculated dates for 2026: March 20 and Sept 22
intersection_dates = ["20/03", "22/09"] 

for i, idx in enumerate([idx1, idx2]):
    # Formats the bilingual label with the specific date
    date_label = f"{label_intersection}\n({intersection_dates[i]})"
    
    ax.annotate(date_label, 
                xy=(dates[idx], seattle_hours[idx]), 
                xytext=(dates[idx], seattle_hours[idx] - 4.5), # Adjusted slightly for text room
                arrowprops=dict(facecolor='black', shrink=0.08, width=1.5, headwidth=8),
                ha='center', fontsize=10, fontweight='bold', color='black')

# Add marker for the Summer Solstice / Hạ chí
ax.annotate('Summer Solstice\nHạ chí (21/06)', 
            xy=(pd.Timestamp('2026-06-21'), 15.8), 
            xytext=(pd.Timestamp('2026-08-15'), 17.5),
            arrowprops=dict(facecolor='black', shrink=0.05, width=1),
            ha='center', fontsize=10)

plt.tight_layout()

# 5. Save
filename = "daylight_intersection.png"
plt.savefig(filename, dpi=300)
print(f"Success! Image saved to: {os.path.abspath(filename)}")