from tinydb import TinyDB
import os
import pandas as pd
import json
import matplotlib.pyplot as plt

# Connect to the drop_oscillation table
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Database', 'database.json')
db = TinyDB(db_path)
drop_osci_table = db.table('drop_oscillation')

# Get all records
data = drop_osci_table.all()

# Parse the JSON string in each record

records = []
for entry in data:
    # The value is a JSON string under the key 'drop_oscillation'
    raw = entry.get('drop_oscillation')
    if raw:
        parsed = json.loads(raw)
        bottle = parsed.get('bottle')
        values = [float(v) for v in parsed.get('drop_oscillation', [])]
        for i, value in enumerate(values):
            records.append({'bottle': bottle, 'time': i, 'value': value})

df = pd.DataFrame(records)


print(df.head())

print("Number of unique bottles:", df['bottle'].nunique())

# Plotting the data
plt.figure(figsize=(10, 5))
for bottle in df['bottle'].unique()[:5]:
    bottle_data = df[df['bottle'] == bottle]
    plt.plot(bottle_data['time'], bottle_data['value'], marker='o', label=f'Bottle {bottle}')
plt.xlabel('Time')
plt.ylabel('Drop Oscillation Value')
plt.title('Drop Oscillation Over Time (First 10 Bottles)')
plt.legend()
plt.grid(True)
plt.show()