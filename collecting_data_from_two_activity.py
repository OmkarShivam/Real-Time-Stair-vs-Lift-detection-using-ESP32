import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report

# Load data from CSV files for each activity
lift_data = pd.read_csv('rate_of_change_data_lift.csv')
stairs_data = pd.read_csv('rate_of_change_data_stairs.csv')

# Split data into training and testing sets
lift_train, lift_test = train_test_split(lift_data, test_size=0.2, random_state=42)
stairs_train, stairs_test = train_test_split(stairs_data, test_size=0.2, random_state=42)

# Combine training and testing data
train_data = pd.concat([lift_train, stairs_train], ignore_index=True)
test_data = pd.concat([lift_test, stairs_test], ignore_index=True)

# Separate features and target variable
X_train = train_data.drop(columns=['activity'])
y_train = train_data['activity']
X_test = test_data.drop(columns=['activity'])
y_test = test_data['activity']

# Train SVM model
svm_model = SVC(kernel='linear', C=1.0)
svm_model.fit(X_train, y_train)

# Evaluate model
y_pred = svm_model.predict(X_test)
report = classification_report(y_test, y_pred)

# Print the classification report
print("Classification Report:")
print(report)
