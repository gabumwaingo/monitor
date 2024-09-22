from flask import Flask, render_template, jsonify
import paho.mqtt.client as mqtt

app = Flask(__name__)

# Store the telemetry data for the drones
drone_data = {}

# MQTT callback for receiving telemetry data
def on_message(client, userdata, message):
    global drone_data
    payload = message.payload.decode("utf-8")
    drone_id, position, speed = parse_payload(payload)
    drone_data[drone_id] = {
        "position": position,
        "speed": speed,
    }

# Function to parse the telemetry payload (assuming it comes as a comma-separated string)
def parse_payload(payload):
    parts = payload.split(',')
    drone_id = parts[0]
    position = [float(parts[1]), float(parts[2])]  # Latitude, Longitude
    speed = float(parts[3])  # Speed in m/s
    return drone_id, position, speed

# Initialize the MQTT client
mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.connect("mqtt_broker_ip", 1883, 60)  # Replace with your MQTT broker IP
mqtt_client.subscribe("drones/telemetry")  # Subscribe to the telemetry topic
mqtt_client.loop_start()  # Start the MQTT client loop in the background

# Route for the dashboard homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to fetch drone data for map visualization
@app.route('/data')
def data():
    return jsonify(drone_data)

if __name__ == '__main__':
    app.run(debug=True)
