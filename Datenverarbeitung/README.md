# Bericht Jan Naidr, Cornelius Brandt, Mats Schulte
Die Messages des MQTT Servers werden mittels paho-mqtt ausgelesen. Die von den verschiedenen Topics empfangenen Messages werden dann nach Topic sortiert und mittels TinyDB in eine database.json Datei abgespeichert. Mit visualizer.py kann ein Plot des Temperaturverlaufs des roten Dispensers erstellt werden. Diese Datei kann aber auf jede beliebige Datenreihe umgeschrieben werden.  
![Temperaturverlauf des roten Dispensers](Database/Plot%20Diespenser%20Red.png)

## Linear Regression Model

Durch das Skript lin_reg.py kann ein Linear Regression Modell mit den Daten aus database.json trainiert werden, um die Größe `final_weight` vorherzusagen.

| Genutzte Spalten         | Modelltyp           | MSE-Wert (Training) | MSE-Wert(Test) |
|--------------------------|---------------------|---------------------|-----------------|
|`vibration index red`, ``fill level grams red``, ``vibration index green``, ``fill level grams green``, ``vibration index blue``, ``fill level grams blue``, ``temperature red``, ``temperature green``, ``temperature blue`` | Lineare Regression  | 0.071|0.1002 |


## Formel für das Modell

final_weight = 0.09026261 * vibration_index_red + 0.00102775 * fill_level_grams_red + 0.09996379 * vibration_index_green + 0.00056406 * fill_level_grams_green + 0.09822221 * virbration_index_blue + 0.00036188 * fill_level_grams_blue + 0.17195129 * temperature_red - 0.00784363 * temperature_green - 0.03339488 * temperature_blue

## Ergebnis
In der Datei [reg_52315859-52316593-52315878.csv](reg_52315859-52316593-52315878.csv) Datei können die Ergebnisse der Linearen Regression für den Datensatz in X.csv eingesehen werden
