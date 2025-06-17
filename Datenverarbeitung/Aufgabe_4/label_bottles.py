from tinydb import TinyDB, Query
import os
import pandas as pd
import matplotlib.pyplot as plt
import json  # Added missing import

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
            records.append({'Bottle': bottle, 'time': i, 'value': value})

df = pd.DataFrame(records)

Bottle = Query()  # Added for TinyDB update

for bottle_id in df['bottle'].unique():
    bottle_data = df[df['bottle'] == bottle_id]
    plt.plot(bottle_data['time'], bottle_data['value'], marker='o', label=f'Bottle {bottle_id}')
    plt.xlabel('Time')
    plt.ylabel('Oscillation Value')
    plt.title(f'Bottle ID: {bottle_id}')
    plt.grid(True)
    # Set fixed x and y limits based on the whole dataset
    plt.xlim(df['time'].min(), df['time'].max())
    plt.ylim(df['value'].min(), df['value'].max())
    plt.show(block=False)
    
    # Ask user for label
    label = input(f"Bottle ID {bottle_id}: Intakt (t) or Broken (f)? [t/f]: ").strip().lower()
    plt.close()
    
    if label == 't':
        is_intakt = True
    elif label == 'f':
        is_intakt = False
    else:
        print("Invalid input, skipping this bottle.")
        continue

    # Update the bottle entry with the label
    # Save the label to a CSV file
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bottle_labels.csv')
    # Check if file exists to determine if header is needed
    write_header = not os.path.exists(csv_path)
    with open(csv_path, 'a', newline='') as f:
        if write_header:
            f.write('bottle,status\n')
        status = is_intakt
        f.write(f'{bottle_id},{status}\n')

print("Labeling complete.")