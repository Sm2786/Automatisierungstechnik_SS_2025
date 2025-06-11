import json
import pandas as pd
import seaborn as sns
import os
import matplotlib.pyplot as plt
import numpy as np


script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, 'database.json')
with open(file_path, 'r') as file:
    data = json.load(file)


# Leeres Dictionary für alle Daten
rows = {}

# Funktion zum Einfügen von Füllständen/Vibrationen
def parse_and_insert(color, dispenser_data):
    for entry in dispenser_data.values():
        entry_json = json.loads(entry[f'dispenser_{color}'])
        bottle = entry_json['bottle']
        vibration = entry_json['vibration-index']
        fill = entry_json['fill_level_grams']
        if bottle not in rows:
            rows[bottle] = {'bottle': bottle}
        rows[bottle][f'vibration index {color}'] = vibration
        rows[bottle][f'fill level grams {color}'] = fill

# Daten aus dispensers
for color in ['red', 'green', 'blue']:
    if f'dispenser_{color}' in data:
        parse_and_insert(color, data[f'dispenser_{color}'])

# Finalgewichte einfügen
for entry in data.get('final_weight', {}).values():
    entry_json = json.loads(entry['final_weight'])
    bottle = entry_json['bottle']
    final_weight = entry_json['final_weight']
    if bottle not in rows:
        rows[bottle] = {'bottle': bottle}
    rows[bottle]['final weight'] = final_weight

# Temperaturdaten verarbeiten
temperature_data = data.get('temperature', {})
temp_by_color = {'red': [], 'green': [], 'blue': []}

# Sammle Temperaturwerte nach Farbe in Reihenfolge
for entry in temperature_data.values():
    parsed = json.loads(entry['temperature'])
    color = parsed['dispenser']
    temp = parsed['temperature_C']
    temp_by_color[color].append(temp)

# Trage Temperaturdaten nach der Reihenfolge in die bottles ein
for color in ['red', 'green', 'blue']:
    bottle_keys = [b for b in rows if f'fill level grams {color}' in rows[b]]
    for bottle, temp in zip(bottle_keys, temp_by_color[color]):
        rows[bottle][f'temperature {color}'] = temp

# DataFrame erstellen
df = pd.DataFrame.from_dict(rows, orient='index')

# Spaltenreihenfolge definieren
columns_order = [
    'bottle', 'vibration index red', 'fill level grams red',
    'vibration index green', 'fill level grams green', 
    'vibration index blue', 'fill level grams blue', 'temperature red', 'temperature green', 'temperature blue',
    'final weight'
]
df = df.reindex(columns=columns_order)
df.reset_index(drop=True, inplace=True)

# Ausgabe 
print(df.head())




#sns.pairplot(df, hue='final weight')
#plt.show()

y = df['final weight']
X = df.drop(['final weight', 'bottle'], axis=1)

y = y.fillna(y.mean())
X = X.fillna(X.mean())

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train.head()

#print(X_train.head())


from sklearn.linear_model import LinearRegression
model = LinearRegression()

model.fit(X_train, y_train)
model.coef_
print("Coefficients:", model.coef_)

y_pred = model.predict(X_train)

#print(y_pred)

df_comparison = pd.DataFrame({'Actual': y_train, 'Predicted': y_pred})


print(df_comparison)

from sklearn.metrics import mean_squared_error
mean_sq_error = mean_squared_error(y_train, y_pred)

#print(mean_sq_error)

y_pred = model.predict(X_test)

mean_sq_error_test = mean_squared_error(y_test, y_pred)
#print(mean_sq_error_test)




# === NEUE PROGNOSE FÜR X.csv ==

# Datei laden
x_path = os.path.join(script_dir, 'X.csv')
X_new = pd.read_csv(x_path)
X_new = X_new.drop('bottle', axis=1)  # Entfernen der 'bottle'-Spalte, falls vorhanden

X_new.columns = X.columns

# Falls nötig: gleiche Preprocessing-Schritte wie im Training
X_new = X_new.fillna(X.mean())  # Oder X_train.mean(), je nach Vorgehen

# Vorhersage mit trainiertem Modell
y_hat = model.predict(X_new)

# In DataFrame umwandeln
df_prediction = pd.DataFrame({
    'Flaschen ID': X_new.index + 1,
    'y_hat': y_hat
})

# Speichern in gewünschter CSV-Datei
df_prediction.to_csv('reg_52315859-52316593-52315878.csv', index=False)  # <- Matrikelnummern anpassen!





