from inference import get_model

class YoloService:
    def __init__(self):
        """
        Initialize Roboflow YOLO model (WORKING VERSION)
        """
        self.model = get_model("object-detection-xfoqq/4")

    def detect(self, image_path: str):
        """
        Run object detection and return raw predictions
        """

        results = self.model.infer(image_path)

        if not results or len(results) == 0:
            return []

        # Roboflow format
        predictions = results[0].predictions
        return predictions
