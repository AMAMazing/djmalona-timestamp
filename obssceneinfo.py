import os
from obswebsocket import obsws, requests, exceptions
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OBS connection details
host = "localhost"
port = "4444"  # Port should be a string if required by the library
password = os.getenv("OBS_PASSWORD")

# Connect to OBS WebSocket
ws = obsws(host, port, password)

try:
    ws.connect()
    print("Connected to OBS WebSocket")

    # Get all scenes and print the structure to understand it
    scenes_response = ws.call(requests.GetSceneList())
    scenes = scenes_response.getScenes()

    print("Scene list structure:")
    for scene in scenes:
        print(scene)  # Print each scene's structure

    # Uncomment the following lines if you see the correct structure and want to proceed
    '''
    # Find the "DJing" scene
    scene_name = "DJing"
    scene_found = False
    for scene in scenes:
        if scene["name"] == scene_name:
            scene_found = True
            print(f"Found scene '{scene_name}'")

            # Get each source item in this scene
            for item in scene["sources"]:
                source_name = item["name"]
                scene_item_id = item["id"]

                # Fetch the transform properties for each source
                transform_response = ws.call(requests.GetSceneItemProperties(item["name"]))
                transform = transform_response.datain

                print(f"\nSource Name: {source_name}")
                print(f"Scene Item ID: {scene_item_id}")
                print("Transform Properties:")
                print(f" - Position (X, Y): ({transform['position']['x']}, {transform['position']['y']})")
                print(f" - Rotation: {transform['rotation']}")
                print(f" - Scale (X, Y): ({transform['scale']['x']}, {transform['scale']['y']})")
                print(f" - Crop (Left, Right, Top, Bottom): ({transform['crop']['left']}, {transform['crop']['right']}, {transform['crop']['top']}, {transform['crop']['bottom']})")

    if not scene_found:
        print(f"Scene '{scene_name}' not found.")
    '''

except exceptions.ConnectionFailure:
    print("Failed to connect to OBS WebSocket. Check if OBS is open and WebSocket server is enabled.")

finally:
    try:
        ws.disconnect()
        print("Disconnected from OBS WebSocket")
    except AttributeError:
        print("No active WebSocket connection to close.")
