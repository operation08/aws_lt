from flask import Flask, request, jsonify, render_template
import os
from lightning_sdk import Studio, Machine, Status

app = Flask(__name__)

@app.route('/')
def index():
    """Serve the index.html as the start page."""
    return render_template('index.html')

@app.route('/control_studio', methods=['POST'])
def control_studio():
    try:
        # Get JSON request data
        data = request.json
        api_key = data.get('api_key', '')
        user_id = data.get('user_id', '')
        username = data.get('username', '')
        instance_type = data.get('instance_type', '')
        action = data.get('action', '')

        # Set environment variables
        os.environ["LIGHTNING_API_KEY"] = api_key or "default_api_key"
        os.environ["LIGHTNING_USER_ID"] = user_id or "default_user_id"

        # Default values
        name = "rag"
        teamspace = "vision-model"
        user = "operation000666"

        # Initialize Studio instance
        s = Studio(name=name, teamspace=teamspace, user=user)


        if action == "start":
            # Check if Studio is already running
            if s.status == Status.Running:
                return jsonify({"message": f"Studio is already running on {s.machine}! Run 'ssh vbot_aws' to access it."})
            try:
                if instance_type == "cpu07":
                    s.start()
                    return jsonify({"message": "Studio started successfully on CPU! Run 'ssh vbot_aws' to access it."})
                elif instance_type == "gpu":
                    s.start(machine=Machine.L4)
                    return jsonify({"message": "Studio started successfully with GPU! Run 'ssh vbot_aws' to access it."})
                else:
                    return jsonify({"message": "Wrong Instance!"})
            except Exception as e:
                return jsonify({"error": f"Failed to start Studio: {str(e).lower().replace('lightning', 'aws')}"}), 400

        elif action == "stop":
            try:
                s.stop()
                return jsonify({"message": "Studio stopped successfully!"})
            except Exception as e:
                return jsonify({"error": f"Failed to stop Studio: {str(e).lower().replace('lightning', 'aws')}"}), 400

        else:
            return jsonify({"error": "Invalid action"}), 400

    except Exception as e:
        return jsonify({"error": f"Server Error: {str(e).lower().replace('lightning', 'aws')}"}), 500

# if __name__ == '__main__':
#     # app.run(debug=True)
#     app.run(host="0.0.0.0", port=5000)
