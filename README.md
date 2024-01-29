![Real_Time_detection_model](https://github.com/OmkarShivam/Real-Time-Stair-vs-Lift-detection-using-ESP32/blob/main/images/realtime.jpg)
# Real-Time-Stair-vs-Lift-detection-using-ESP32

This project uses an ESP32 microcontroller and a machine-learning model to implement a real-time activity detection system. The ESP32 collects sensor data (gyroscope and altitude) and sends it to a server running on a computer. The server then processes the data, calculates the rate of change for each sensor reading, and uses a trained Support Vector Machine (SVM) model to predict the activity.

## Components

- **ESP32 Microcontroller**: Collects sensor data (gyroscope and altitude) and sends it to the server over Wi-Fi.
- **Server**: Receives data from the ESP32, calculates the rate of change, predicts the activity using a trained SVM model, and sends the prediction back to the ESP32.
- **Machine Learning Model**: Trained SVM model used for activity prediction.

## Workflow

1. The ESP32 collects sensor data and sends it to the server.
2. The server receives the data, calculates the rate of change for each sensor reading, and predicts the activity using the trained model.
3. The predicted activity is sent back to the ESP32, which controls LEDs based on the prediction.

## Files

- `Sending_data_from_esp32.cpp`: C++ code for the ESP32 microcontroller.
- `Collecting_the_data.py`: Python script for the server.
- `SVM.py`: Jupyter Notebook for training the SVM model.
- `combined_data.csv`: Preprocessed sensor data used for model training.
- `combined_model.pkl`: Trained SVM model saved using joblib.

## Usage

1. Flash the `Sending_data_from_esp32.cpp` sketch to the ESP32 microcontroller.
2. Run the `Collecting_the_data.py` script on a computer connected to the same network as the ESP32.
3. Train the SVM model using the `SVM.py` notebook and save the trained model as `combined_model.pkl`.
4. Upload the `combined_data.csv` file containing preprocessed sensor data for training the model.

## Dependencies

- Arduino IDE for ESP32 development.
- Python 3.10.11 with libraries:  `socket` , `numpy`, `pandas`, `scikit-learn`, `joblib`.

## License

This project is licensed under the [MIT License](LICENSE).
