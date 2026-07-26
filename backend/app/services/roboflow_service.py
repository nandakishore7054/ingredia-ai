"""
Roboflow Hosted Inference Service
==================================
Replaces the local `inference` SDK with direct REST API calls to the
Roboflow serverless hosted inference endpoint.

This keeps CV inference completely server-side and never exposes
the API key to the frontend. It returns structured detection results
including ingredient names, confidence scores, and bounding boxes.
"""

import os
import base64
import httpx
import logging

logger = logging.getLogger(__name__)

# Default confidence threshold — anything below is discarded
CONFIDENCE_THRESHOLD = 0.40


class RoboflowService:
    def __init__(self):
        self.api_key = os.getenv("ROBOFLOW_API_KEY", "")
        self.model_url = os.getenv(
            "ROBOFLOW_MODEL_URL",
            "https://serverless.roboflow.com/object-detection-xfoqq/4"
        )

        if not self.api_key:
            logger.warning(
                "ROBOFLOW_API_KEY not set. Ingredient detection will fail."
            )

    async def detect(self, image_path: str) -> list[dict]:
        """
        Send an image to the Roboflow Hosted Inference API and return
        structured predictions.

        Returns a list of dicts:
        [
            {
                "ingredient": "tomato",
                "confidence": 0.92,
                "bbox": {"x": 120, "y": 80, "width": 200, "height": 150}
            },
            ...
        ]
        """
        if not self.api_key:
            logger.error("Cannot run detection: ROBOFLOW_API_KEY is missing.")
            return []

        try:
            # Read and base64-encode the image
            with open(image_path, "rb") as f:
                image_data = base64.b64encode(f.read()).decode("utf-8")

            # Call the Roboflow serverless inference endpoint
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.model_url,
                    params={"api_key": self.api_key},
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                    data=image_data,
                )

            if response.status_code != 200:
                logger.error(
                    f"Roboflow API returned {response.status_code}: {response.text}"
                )
                return []

            data = response.json()
            logger.info(f"RAW ROBOFLOW RESPONSE for {image_path}: {data}")

            predictions = data.get("predictions", [])
            logger.info(f"Raw predictions count before threshold: {len(predictions)}")

            # Parse and filter by confidence threshold
            results = []
            seen_ingredients = set()

            for pred in predictions:
                confidence = pred.get("confidence", 0)
                label = pred.get("class", "unknown").lower().strip()

                if confidence < CONFIDENCE_THRESHOLD:
                    continue

                results.append({
                    "ingredient": label,
                    "confidence": round(confidence, 2),
                    "bbox": {
                        "x": pred.get("x", 0),
                        "y": pred.get("y", 0),
                        "width": pred.get("width", 0),
                        "height": pred.get("height", 0),
                    },
                })
                seen_ingredients.add(label)

            logger.info(
                f"Roboflow detected {len(results)} objects "
                f"({len(seen_ingredients)} unique ingredients)"
            )
            return results

        except httpx.TimeoutException:
            logger.error("Roboflow API request timed out.")
            return []
        except Exception as e:
            logger.error(f"Roboflow detection failed: {str(e)}")
            return []


# Singleton instance — imported by main.py
roboflow_service = RoboflowService()
