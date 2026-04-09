import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB

# Create models directory
os.makedirs('models', exist_ok=True)

# Load data (Make sure you have the 'data' folder with the CSVs)
train_df = pd.read_csv('data/training_data.csv')

if 'Unnamed: 133' in train_df.columns:
    train_df = train_df.drop(columns=['Unnamed: 133'])

X = train_df.drop('prognosis', axis=1)
y = train_df['prognosis']

# Train and save models
models = {
    'randomforest': RandomForestClassifier(n_estimators=100),
    'svm': SVC(kernel='linear', probability=True),
    'naivebayes': GaussianNB()
}

for name, model in models.items():
    print(f"Training {name}...")
    model.fit(X, y)
    joblib.dump(model, f'models/{name}_model.pkl')

# Save the list of symptoms
joblib.dump(X.columns.tolist(), 'models/symptoms_list.pkl')
print("✅ All models trained and saved successfully in the 'models' folder!")
