import math
from operator import itemgetter
from ultralytics import YOLO
class LicensePlateReader:
    def __init__(self, model_path):
        # Load a model
        self.model = YOLO(model_path)  # pretrained YOLOv5 model

        # Define your class labels based on the order you trained your model
        self.class_labels = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def detect(self, img_path):
        # Run batched inference on a list of images
        results = self.model([img_path])  # return a list of Results objects
        
        # Initialize list to hold characters and their mid-points
        characters = []

        for result in results:
            print('results of yolo_lpr: ', len(result))
            # Get bounding boxes and corresponding class probabilities
            detections = result.boxes.data  # [x1, y1, x2, y2, prob, label]

            # Loop over all detections
            for det in detections:
                # Calculate mid-point coordinates
                mid_x = (det[0].item() + det[2].item()) / 2
                mid_y = (det[1].item() + det[3].item()) / 2

                # Append character, mid-point coordinates and norm to characters list
                characters.append((self.class_labels[int(det[5])], mid_x, mid_y, round(math.sqrt(mid_x**2 + mid_y**2), 3)))

        # Sort characters based on y position
        characters.sort(key=itemgetter(2))  # sort by y-coordinate (mid_y)

        # Initialize final plate string and anchor
        final_plate_str = ""
        anchor = characters[0][2]  # start with the first y-coordinate
        max_diff = 5  # max y-difference to consider characters as in the same line

        # Initialize current line
        current_line = []

        # Loop over all characters
        for char, mid_x, mid_y, _ in characters:
            # If current character is in the same line as the previous one
            if abs(mid_y - anchor) <= max_diff:
                current_line.append((char, mid_x, mid_y))
                anchor = (anchor + mid_y) / 2
            else:
                # If new line starts, sort the previous line by x and append to final plate string
                current_line.sort(key=itemgetter(1))  # sort by x-coordinate
                final_plate_str += "".join([c for c, _, _ in current_line])
                # Reset current line and anchor
                current_line = [(char, mid_x, mid_y)]
                anchor = mid_y

        # Don't forget the last line
        if current_line:
            current_line.sort(key=itemgetter(1))  # sort by x-coordinate
            final_plate_str += "".join([c for c, _, _ in current_line])

        print('final_plate_str: ', final_plate_str)
        return final_plate_str
