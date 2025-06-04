import json
import matplotlib.pyplot as plt
import os

# Path to your database.json
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json')

# Load JSON data
with open(db_path, 'r') as f:
    data = json.load(f)

# Extract temperature_C and time for dispenser red
times = []
temperatures = []

for entry in data["temperature"].values():
    record = json.loads(entry["temperature"])
    if record["dispenser"] == "red":
        times.append(record["time"])
        temperatures.append(record["temperature_C"])

# Plot
plt.figure(figsize=(10, 5))
plt.plot(times, temperatures, marker='o', color='red')
plt.xlabel('Time')
plt.ylabel('Temperature (°C)')
plt.title('Temperature Over Time - Dispenser Red')
plt.grid(True)
plt.show()