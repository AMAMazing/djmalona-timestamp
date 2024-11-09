import os
from obswebsocket import obsws, requests, exceptions
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OBS connection details
host = "localhost"  # Should be localhost for local connections
port = '4444'         # Confirm this matches the port in OBS WebSocket settings
password = os.getenv("OBS_PASSWORD")  # Ensure .env file contains the correct password

# Connect to OBS WebSocket
ws = obsws(host, port, password)

try:
    ws.connect()
    print("Connected to OBS WebSocket")

    # Your transform and scene change code here
    # Example: Switch to a specific scene
    scene_name = "Your Scene Name"
    ws.call(requests.SetCurrentScene(scene_name))
    print(f"Switched to scene: {scene_name}")

except exceptions.ConnectionFailure:
    print("Failed to connect to OBS WebSocket. Check if OBS is open and WebSocket server is enabled.")

finally:
    try:
        ws.disconnect()
        print("Disconnected from OBS WebSocket")
    except AttributeError:
        # If ws.disconnect() fails due to no connection, handle it gracefully
        print("No active WebSocket connection to close.")
