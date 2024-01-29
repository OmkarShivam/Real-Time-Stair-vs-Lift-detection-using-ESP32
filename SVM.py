import socket
import pandas as pd
from joblib import load as load_model

# Set up TCP/IP socket
ESP32_IP = '192.168.137.242'
ESP32_PORT = 8080

# Load the trained SVM model
svm_model = load_model('svm_model.pkl')

try:
    # Connect to ESP32
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((ESP32_IP, ESP32_PORT))

        while True:
            collected_datasets = []

            # Collect two datasets
            for _ in range(2):
                data = client_socket.recv(1024)
                if not data:
                    break

                decoded_data = data.decode().strip()
                print("Decoded Data:", decoded_data)
                if decoded_data:
                    # Split the data
                    data_parts = decoded_data.split(',')
                    print("Data Parts:", data_parts)

                    if len(data_parts) == 5:  # Ensure 5 values (timestamp, gyroX, gyroY, gyroZ, altitude)
                        timestamp = int(data_parts[0])
                        sensor_values = list(map(float, data_parts[1:]))
                        collected_datasets.append((timestamp, sensor_values))
                    else:
                        print("Invalid data format received")
                        continue

            # Once two datasets are collected
            if len(collected_datasets) == 2:
                # Calculate rate of change for each dataset
                for i in range(1, len(collected_datasets)):
                    dataset_1 = collected_datasets[i-1]
                    dataset_2 = collected_datasets[i]

                    delta_time = dataset_2[0] - dataset_1[0]

                    gyro_rate_of_change = [(curr_val - last_val) / delta_time for curr_val, last_val in zip(dataset_2[1][:3], dataset_1[1][:3])]
                    altitude_rate_of_change = (dataset_2[1][3] - dataset_1[1][3]) / delta_time

                    # Create DataFrame with rate of change data
                    rate_of_change_df = pd.DataFrame([gyro_rate_of_change + [altitude_rate_of_change]],
                                                     columns=['gyroX_rate_of_change', 'gyroY_rate_of_change', 'gyroZ_rate_of_change', 'altitude_rate_of_change'])

                    # Predict activity using the trained SVM model
                    predicted_activity = svm_model.predict(rate_of_change_df)
                    print("Predicted Activity for Dataset", i, ":", predicted_activity[0])

                    # Send prediction to ESP32
                    client_socket.send(predicted_activity[0].encode())

                # Receive model performance metrics from ESP32
                accuracy = client_socket.recv(1024).decode()
                precision = client_socket.recv(1024).decode()
                recall = client_socket.recv(1024).decode()
                f1_score = client_socket.recv(1024).decode()

                print("Model Performance Metrics:")
                print("Accuracy:", accuracy)
                print("Precision:", precision)
                print("Recall:", recall)
                print("F1 Score:", f1_score)

except Exception as e:
    print("An error occurred:", e)
