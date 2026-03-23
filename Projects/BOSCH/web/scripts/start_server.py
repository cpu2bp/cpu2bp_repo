# Save this as server.py on the remote PC
from flask import Flask, jsonify
from flask_cors import CORS # You'll need to install this: pip install Flask-Cors
import subprocess
import re

app = Flask(__name__)
# This is crucial! It allows your GitHub page to request data from this server.
CORS(app)

def get_active_user():
    """
    Uses the 'query user' command to find an active user session.
    Returns the username of the first active session found, or None.
    """
    try:
        # Run the 'query user' command, don't check for exit code as 1 is a valid outcome (no users)
        result = subprocess.run(['query', 'user'], capture_output=True, text=True)
        output = result.stdout

        # If the command returns exit code 1 and a specific message, it means no one is logged on.
        if result.returncode == 1 and 'No User exists' in output:
            return None

        # Process each line of the output
        lines = output.strip().split('\n')
        for line in lines[1:]: # Skip the header line
            # A simple regex to find a line with 'Active' state
            # This is more robust than splitting by spaces which can be inconsistent
            if re.search(r'\s+Active\s+', line):
                # The username is the first word on the line
                username = line.split()[0]
                # If the username starts with '>', it's the current session, remove it
                if username.startswith('>'):
                    username = username[1:]
                return username
    except (FileNotFoundError, IndexError) as e:
        # Handle cases where 'query' command is not found or other parsing errors
        print(f"Could not query user: {e}")
        return None
    return None


@app.route('/api/userinfo')
def get_user_info():
    active_user = get_active_user()
    if active_user:
        data = {'username': active_user, 'status': 'logged_in'}
    else:
        data = {'username': None, 'status': 'no_active_session'}
    return jsonify(data)

if __name__ == '__main__':
    # This makes the server accessible on your local network
    app.run(host='0.0.0.0', port=5000)