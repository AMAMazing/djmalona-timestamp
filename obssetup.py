import os
from obswebsocket import obsws, requests, exceptions
from dotenv import load_dotenv

active_monitor = '1440p'

# Load environment variables from .env file
load_dotenv()

# OBS connection details
host = "localhost"
port = "4455"
password = os.getenv("OBS_PASSWORD")

# Connect to OBS WebSocket
ws = obsws(host, port, password)

# Base transforms for 1080p monitor
transform_1080p = {
    "Rekordbox Capture 1": {"positionX": 600.0, "positionY": 500.0, "rotation": 0.0, "scaleX": 1.8, "scaleY": 1.8, "cropLeft": 0, "cropRight": 1315, "cropTop": 195, "cropBottom": 812},
    "Rekordbox Capture 2": {"positionX": 600.0, "positionY": 0.0, "rotation": 0.0, "scaleX": 1.8, "scaleY": 1.8, "cropLeft": 1018, "cropRight": 300, "cropTop": 195, "cropBottom": 812},
    "Rekordbox Capture 3": {"positionX": 300.0, "positionY": 291.0, "rotation": 0.0, "scaleX": 1.8519, "scaleY": 1.85, "cropLeft": 307, "cropRight": 959, "cropTop": 193, "cropBottom": 595},
    "Rekordbox Capture 4": {"positionX": 0.0, "positionY": 291.0, "rotation": 0.0, "scaleX": 1.8519, "scaleY": 1.85, "cropLeft": 959, "cropRight": 907, "cropTop": 193, "cropBottom": 595}
}

# Calculated scaling factor for crops
yadjust = 106
xadjust = 310

# Calculate 1440p transforms by applying the crop scaling factor
transform_1440p = {}
for key, values in transform_1080p.items():
    transform_1440p[key] = {
        "positionX": values["positionX"],
        "positionY": values["positionY"],
        "rotation": values["rotation"],
        "scaleX": values["scaleX"],
        "scaleY": values["scaleY"],
        "cropLeft": int(values["cropLeft"] + xadjust),
        "cropRight": int(values["cropRight"] + xadjust),
        "cropTop": int(values["cropTop"] + yadjust),
        "cropBottom": int(values["cropBottom"] + yadjust)
    }

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
