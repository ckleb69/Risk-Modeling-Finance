import pandas as pd

# Load and filter
df = pd.read_csv(r"C:\Users\Connor\Downloads\CleanSZ.csv")
df = df[(df['PitchCall'] == 'InPlay') & df['ExitSpeed'].notna() & df['Angle'].notna()]

# Compute 5th and 95th percentiles for Launch Angle and Exit Velocity
percentiles = df[['ExitSpeed', 'Angle']].quantile([0.05, 0.95])
print("5th–95th percentile range for Exit Velocity and Launch Angle:\n")
print(percentiles)

# Alternatively, print cleanly formatted ranges
ev_low, ev_high = percentiles.loc[0.05, 'ExitSpeed'], percentiles.loc[0.95, 'ExitSpeed']
la_low, la_high = percentiles.loc[0.05, 'Angle'], percentiles.loc[0.95, 'Angle']

print(f"\nExit Velocity 90% range: {ev_low:.2f} – {ev_high:.2f} mph")
print(f"Launch Angle   90% range: {la_low:.2f} – {la_high:.2f}°")