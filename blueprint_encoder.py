import base64
import zlib
import json
from base64 import encode

base = {
    "blueprint": {
        "icons": [],
        "entities": [],
        "wires": [],
        "item": "blueprint",
        "version": 562949953945601
    }
}
def encode(blueprint_json, version_byte=0):
    # Step 1: Convert the blueprint JSON to a string
    json_string = json.dumps(blueprint_json)

    # Step 2: Compress the JSON string using zlib
    compressed_data = zlib.compress(json_string.encode('utf-8'), level=9)

    # Step 3: Base64 encode the compressed data
    encoded_data = base64.b64encode(compressed_data).decode('utf-8')

    # Step 4: Prepend the version byte
    encoded_blueprint_string = f"{version_byte}{encoded_data}"

    return encoded_blueprint_string

def decode_blueprint_string(blueprint_string):
    # Step 1: Skip the first byte (version byte)
    # The first byte is simply the first character of the string
    encoded_data = blueprint_string[1:]

    # Step 2: Base64 decode
    try:
        decoded_data = base64.b64decode(encoded_data)
    except Exception as e:
        raise ValueError("Failed to decode Base64: " + str(e))

    # Step 3: Decompress using zlib
    try:
        decompressed_data = zlib.decompress(decoded_data)
    except Exception as e:
        raise ValueError("Failed to decompress data: " + str(e))

    # Convert bytes to string
    json_string = decompressed_data.decode('utf-8')

    # Optionally, parse the JSON string to a Python dictionary
    blueprint_json = json.loads(json_string)

    return blueprint_json

def decode(blueprint_string):
    try:

        blueprint_json = decode_blueprint_string(blueprint_string)
        return json.dumps(blueprint_json, indent=4)
    except ValueError as e:
        return e
if __name__ == "__main__":
    # Sample blueprint JSON
    sample_blueprint = {
    "blueprint": {
        "icons": [
            {
                "signal": {
                    "name": "arithmetic-combinator"
                },
                "index": 1
            }
        ],
        "entities": [],
        "wires": [],
        "item": "blueprint",
        "version": 562949953945601
    }
}

    # Encode the blueprint
    encoded_string = encode(sample_blueprint)
    print("Encoded Blueprint String:")
    print(encoded_string)

def print_help():
    print(
    """
    1 - красный вход
    2 - зелёный вход
    3 - красный выход
    4 - зелёный выход
    """)
