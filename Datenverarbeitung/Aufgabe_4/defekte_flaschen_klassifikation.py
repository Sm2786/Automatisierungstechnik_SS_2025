import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tinydb import TinyDB
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

# === 1. Daten einlesen und Zeitreihen extrahieren ===
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Database', 'database.json')
db = TinyDB(db_path)
drop_osci_table = db.table('drop_oscillation')

records = []
for entry in drop_osci_table.all():
    raw = entry.get('drop_oscillation')
    if raw:
        parsed = json.loads(raw)
        bottle = parsed.get('bottle')
        values = [float(v) for v in parsed.get('drop_oscillation', [])]
        for i, value in enumerate(values):
            records.append({'bottle': bottle, 'time': i, 'value': value})

df = pd.DataFrame(records)

# === 2. Feature Engineering ===
feature_rows = []
for bottle_id in df['bottle'].unique():
    values = df[df['bottle'] == bottle_id]['value'].values
    fft = np.fft.fft(values)
    
    features = {
        'bottle': bottle_id,
        'mean': np.mean(values),
        'std': np.std(values),
        'fft_10Hz': np.abs(fft[10]) if len(fft) > 10 else 0,
        'fft_20Hz': np.abs(fft[20]) if len(fft) > 20 else 0,
    }
    feature_rows.append(features)

features_df = pd.DataFrame(feature_rows)

# === 3. Labels laden ===
labels_df = pd.read_csv('Datenverarbeitung/Aufgabe 4/bottle_labels.csv')
labels_df['status'] = labels_df['status'].astype(int)  # True/False -> 1/0

# === 4. Features & Labels zusammenführen ===
features_df['bottle'] = features_df['bottle'].astype(str)
labels_df['bottle'] = labels_df['bottle'].astype(str)

data_df = features_df.merge(labels_df, on='bottle')

print("data_df shape:", data_df.shape)
print(data_df.head())

# === 5. Modelltraining mit verschiedenen Feature-Sets ===
feature_sets = {
    'mean': ['mean'],
    'mean_std': ['mean', 'std'],
    'fft_only': ['fft_10Hz', 'fft_20Hz'],
    'all_features': ['mean', 'std', 'fft_10Hz', 'fft_20Hz']
}

results = []

models = {
    'Random Forest': RandomForestClassifier(random_state=42),
    'KNN': KNeighborsClassifier(),
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'Decision Tree': DecisionTreeClassifier(random_state=42)
}

for name, features in feature_sets.items():
    X = data_df[features]
    y = data_df['status']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    for model_name, model in models.items():
        clf = model
        clf.fit(X_train, y_train)

        y_train_pred = clf.predict(X_train)
        y_test_pred = clf.predict(X_test)

        f1_train = f1_score(y_train, y_train_pred)
        f1_test = f1_score(y_test, y_test_pred)

        results.append({
            'Genutzte Features': ", ".join(features),
            'Modell-Typ': model_name,
            'F1-Score (Training)': round(f1_train, 3),
            'F1-Score (Test)': round(f1_test, 3)
        })
        cm = confusion_matrix(y_test, y_test_pred)
        fig_name = f"CM_{name}_{model_name}".replace(" ", "_")
        if 'conf_matrices' not in locals():
            conf_matrices = []
        conf_matrices.append((fig_name, cm, y_test.unique()))

# === 6. Konfusionsmatrizen plotten ===
# Arrange confusion matrices in a 4x4 grid
rows, cols = 4, 4
fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 5 * rows))

# Flatten axes for easy iteration
axes_flat = axes.flatten()

for idx, (fig_name, cm, labels) in enumerate(conf_matrices):
    ax = axes_flat[idx]
    im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    ax.set_title(f'Confusion Matrix:\n{fig_name}', fontsize=10)
    tick_marks = np.arange(len(labels))
    ax.set_xticks(tick_marks)
    ax.set_yticks(tick_marks)
    ax.set_xticklabels(labels, rotation=45)
    ax.set_yticklabels(labels)
    thresh = cm.max() / 2.
    for i, j in np.ndindex(cm.shape):
        ax.text(j, i, cm[i, j], ha='center', va='center',
                color='white' if cm[i, j] > thresh else 'black', fontsize=10)
    ax.set_ylabel('True label')
    ax.set_xlabel('Predicted label')

# Hide unused subplots
for ax in axes_flat[len(conf_matrices):]:
    ax.axis('off')

#fig.colorbar(im, ax=axes_flat[:len(conf_matrices)], fraction=0.02, pad=0.04)
plt.tight_layout()
# plt.savefig("all_confusion_matrices.png")
plt.show()

# === 6. Dokumentationstabelle ===
results_df = pd.DataFrame(results)

print("\nErgebnistabelle:")
print(results_df.to_string(index=False))

# Tabelle als Markdown ausgeben
print("\nMarkdown-Tabelle:\n")
print(results_df.to_markdown(index=False))
