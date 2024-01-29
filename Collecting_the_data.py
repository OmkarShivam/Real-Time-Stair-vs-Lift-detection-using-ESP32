import socket

# Set up TCP/IP socket
ESP32_IP = '192.168.137.242'
ESP32_PORT = 8080

# Function to receive data and save to CSV based on activity
def receive_and_save_data():
    # Connect to ESP32
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ESP32_IP, ESP32_PORT))

    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            decoded_data = data.decode().strip()
            if decoded_data:
                # Split the data
                data_parts = decoded_data.split(',')
                timestamp = int(data_parts[0])
                sensor_values = ','.join(data_parts[1:8])
                activity = data_parts[8]

                # Write data to CSV file
                with open('realtime_data.csv', 'a') as file:
                    # Check if file is empty
                    file.seek(0, 2)
                    if file.tell() == 0:
                        file.write("timestamp,accelX,accelY,accelZ,gyroX,gyroY,gyroZ,altitude,activity\n")
                    file.write(f"{timestamp},{sensor_values},{activity}\n")

    except KeyboardInterrupt:
        pass

    finally:
        # Close the client socket
        client_socket.close()

# Call the function to receive and save data
receive_and_save_data()
