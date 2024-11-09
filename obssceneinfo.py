import os
from obswebsocket import obsws, requests, exceptions
from dotenv import load_dotenv
from difflib import get_close_matches

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

    # Get all scenes
    scenes_response = ws.call(requests.GetSceneList())
    scenes = scenes_response.getScenes()

    # Build a list of scene names
    scene_names = [scene['sceneName'] for scene in scenes]
    print("Available scenes:")
    for name in scene_names:
        print(f" - {name}")

    # Input scene name
    input_scene_name = "DJing (1080 no scaling)"

    # Find the closest match to the input scene name
    closest_matches = get_close_matches(input_scene_name, scene_names, n=1, cutoff=0.0)

    if closest_matches:
        matched_scene_name = closest_matches[0]
        print(f"Using scene '{matched_scene_name}' as the closest match to '{input_scene_name}'")
    else:
        print(f"No close match found for scene '{input_scene_name}'")
        ws.disconnect()
        exit()

    # Get the scene items (sources) in the matched scene
    scene_items_response = ws.call(requests.GetSceneItemList(sceneName=matched_scene_name))
    scene_items = scene_items_response.getSceneItems()

    # For each scene item, get the transform properties
    for item in scene_items:
        source_name = item['sourceName']
        scene_item_id = item['sceneItemId']

        # Get the transform properties
        transform_response = ws.call(requests.GetSceneItemTransform(
            sceneName=matched_scene_name,
            sceneItemId=scene_item_id
        ))
        transform = transform_response.datain['sceneItemTransform']  # Adjusted line

        print(f"\nSource Name: {source_name}")
        print(f"Scene Item ID: {scene_item_id}")
        print("Transform Properties:")
        print(f" - Position (X, Y): ({transform['positionX']}, {transform['positionY']})")
        print(f" - Rotation: {transform['rotation']}")
        print(f" - Scale (X, Y): ({transform['scaleX']}, {transform['scaleY']})")
        print(f" - Crop (Left, Right, Top, Bottom): ({transform['cropLeft']}, {transform['cropRight']}, {transform['cropTop']}, {transform['cropBottom']})")

except exceptions.ConnectionFailure:
    print("Failed to connect to OBS WebSocket. Check if OBS is open and WebSocket server is enabled.")

finally:
    try:
        ws.disconnect()
        print("Disconnected from OBS WebSocket")
    except AttributeError:
        print("No active WebSocket connection to close.")
