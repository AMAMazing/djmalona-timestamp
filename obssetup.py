import os
from obswebsocket import obsws, requests, exceptions
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OBS connection details
host = "localhost"
port = "4444"
password = os.getenv("OBS_PASSWORD")

# Connect to OBS WebSocket
ws = obsws(host, port, password)

# Define transforms for 1440p and 1080p monitors
transform_1440p = {
    "Rekordbox Capture 1": {"positionX": 0.0, "positionY": 0.0, "rotation": 0.0, "scaleX": 0.5, "scaleY": 0.5, "cropLeft": 0, "cropRight": 0, "cropTop": 0, "cropBottom": 0},
    "Rekordbox Capture 2": {"positionX": 1280.0, "positionY": 0.0, "rotation": 0.0, "scaleX": 0.5, "scaleY": 0.5, "cropLeft": 0, "cropRight": 0, "cropTop": 0, "cropBottom": 0},
    "Rekordbox Capture 3": {"positionX": 0.0, "positionY": 720.0, "rotation": 0.0, "scaleX": 0.5, "scaleY": 0.5, "cropLeft": 0, "cropRight": 0, "cropTop": 0, "cropBottom": 0},
    "Rekordbox Capture 4": {"positionX": 1280.0, "positionY": 720.0, "rotation": 0.0, "scaleX": 0.5, "scaleY": 0.5, "cropLeft": 0, "cropRight": 0, "cropTop": 0, "cropBottom": 0}
}

transform_1080p = {
    "Rekordbox Capture 1": {"positionX": 0.0, "positionY": 1080.0, "rotation": 270.0, "scaleX": 1.8, "scaleY": 1.8, "cropLeft": 0, "cropRight": 1315, "cropTop": 195, "cropBottom": 812},
    "Rekordbox Capture 2": {"positionX": 1920.0, "positionY": 0.0, "rotation": 90.0, "scaleX": 1.8, "scaleY": 1.8, "cropLeft": 1018, "cropRight": 300, "cropTop": 195, "cropBottom": 812},  # Specific transform for Rekordbox Capture 2
    "Rekordbox Capture 3": {"positionX": 90.0, "positionY": 291.0, "rotation": 0.0, "scaleX": 1.8519, "scaleY": 1.8513, "cropLeft": 907, "cropRight": 959, "cropTop": 193, "cropBottom": 595},
    "Rekordbox Capture 4": {"positionX": 1730.0, "positionY": 291.0, "rotation": 0.0, "scaleX": 1.8519, "scaleY": 1.8513, "cropLeft": 959, "cropRight": 907, "cropTop": 193, "cropBottom": 595}
}

# Set the desired monitor resolution (change between '1440p' and '1080p')
active_monitor = '1080p'  # or '1440p' depending on which monitor you are using

# Select the appropriate transform set
transforms = transform_1440p if active_monitor == '1440p' else transform_1080p

try:
    ws.connect()
    print("Connected to OBS WebSocket")

    # Get scene items for "DJing"
    scene_name = "DJing"
    scene_items_response = ws.call(requests.GetSceneItemList(sceneName=scene_name))
    scene_items = scene_items_response.getSceneItems()

    # Apply the correct transform to each Rekordbox source based on monitor resolution
    for item in scene_items:
        source_name = item['sourceName']
        scene_item_id = item['sceneItemId']

        if source_name in transforms:
            transform = transforms[source_name]
            ws.call(requests.SetSceneItemTransform(
                sceneName=scene_name,
                sceneItemId=scene_item_id,
                sceneItemTransform={
                    "positionX": transform["positionX"],
                    "positionY": transform["positionY"],
                    "rotation": transform["rotation"],
                    "scaleX": transform["scaleX"],
                    "scaleY": transform["scaleY"],
                    "cropLeft": transform["cropLeft"],
                    "cropRight": transform["cropRight"],
                    "cropTop": transform["cropTop"],
                    "cropBottom": transform["cropBottom"]
                }
            ))
            print(f"Applied {active_monitor} transform to '{source_name}'")

except exceptions.ConnectionFailure:
    print("Failed to connect to OBS WebSocket. Check if OBS is open and WebSocket server is enabled.")

finally:
    try:
        ws.disconnect()
        print("Disconnected from OBS WebSocket")
    except AttributeError:
        print("No active WebSocket connection to close.")
