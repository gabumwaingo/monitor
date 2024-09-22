from flask import Flask, render_template, jsonify
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from extensions import db
from models.user_model import User
from models.agent_model import Agent
from config import Config
import paho.mqtt.client as mqtt

app = Flask(__name__)
app.config.from_object(Config)

# Initialize SQLAlchemy and Flask-Admin
db.init_app(app)
admin = Admin(app, name='Dashboard', template_mode='bootstrap4')

# Add views for models to Flask-Admin
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Agent, db.session))

# Store the drone telemetry data (position, speed)
drone_data = {}

@app.route('/update_drone_data', methods=['POST'])
def update_drone_data():
    data = request.json  # Assume data comes in JSON format
    drone_id = data['drone_id']
    position = data['position']
    speed = data['speed']
    
    # Update the drone's data
    drone_data[drone_id] = {
        'position': position,
        'speed': speed
    }
    
    return jsonify({"message": "Drone data updated successfully"}), 200

# Route to serve the drone data to the frontend
@app.route('/drone_data')
def drone_data_route():
    return jsonify(drone_data)

@app.route('/')
def index():
    user_count = User.query.count()
    agent_count = Agent.query.count()
    return render_template('index.html', user_count=user_count, agent_count=agent_count)

# Create the tables in the database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
