import base64
import requests

def upload_to_freeimage_host(image_path):
    with open(image_path, "rb") as image_file:
        b64_image = base64.b64encode(image_file.read()).decode('utf-8')

    url = "https://freeimage.host/api/1/upload"
    # Using a public API key for freeimage.host
    data = {
        "key": "6d207e02198a847aa98d0a2a901485a5",
        "action": "upload",
        "source": b64_image,
        "format": "json"
    }

    response = requests.post(url, data=data)
    try:
        return response.json()['image']['url']
    except Exception as e:
        return f"Upload failed: {response.text}"

print(upload_to_freeimage_host("/tmp/hologram_ui_test.png"))
