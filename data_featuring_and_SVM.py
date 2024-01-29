import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import LabelEncoder
import joblib

# Load the preprocessed data
data = pd.read_csv("combined_data.csv")

# Encode the activity labels
label_encoder = LabelEncoder()
data['activity_encoded'] = label_encoder.fit_transform(data['activity'])

# Select features for training
features = ['altitude_rate_of_change', 'gyroX_rate_of_change', 'gyroY_rate_of_change', 'gyroZ_rate_of_change']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data[features], data['activity_encoded'], test_size=0.2, random_state=42)

# Train a single SVM model for both activities
model = SVC(kernel='rbf')
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')

print("Accuracy for the Combined Model:", accuracy)
print("Precision for the Combined Model:", precision)
print("Recall for the Combined Model:", recall)
print("F1-score for the Combined Model:", f1)

# Save the trained model for later use
joblib.dump(model, 'combined_model.pkl')
