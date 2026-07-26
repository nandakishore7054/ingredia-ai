import asyncio
import os
import sys
import json
import base64
import httpx

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("ROBOFLOW_API_KEY", "")
MODEL_URL = os.getenv("ROBOFLOW_MODEL_URL", "https://serverless.roboflow.com/object-detection-xfoqq/4")

async def test_raw_api(image_path: str):
    print(f"\n==================================================")
    print(f"RAW HTTP TEST FOR: {os.path.basename(image_path)}")
    print(f"==================================================")
    
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    # 1. Standard call (default confidence threshold on Roboflow server)
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(
            MODEL_URL,
            params={"api_key": API_KEY},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=image_data,
        )
        print(f"HTTP Status: {resp.status_code}")
        print("Raw Response (Default Params):")
        print(json.dumps(resp.json(), indent=2))

    # 2. Call with confidence=0.01 parameter to see ALL raw bounding box candidate predictions
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp_low = await client.post(
            MODEL_URL,
            params={"api_key": API_KEY, "confidence": "0.01"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=image_data,
        )
        print("\nRaw Response (with confidence=0.01 parameter):")
        print(json.dumps(resp_low.json(), indent=2))

async def main():
    temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp_uploads")
    for fname in ["onion.jpeg", "camera.jpg", "WIN_20260725_19_57_13_Pro.jpg"]:
        fpath = os.path.join(temp_dir, fname)
        if os.path.exists(fpath):
            await test_raw_api(fpath)

if __name__ == "__main__":
    asyncio.run(main())
