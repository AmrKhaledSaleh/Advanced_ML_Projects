import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.models import Sequential
# from tensorflow.keras.models import model_from_json, load_model


class COD:
    def __init__(self, model_type='cnn'):
        # Define the base model with pre-trained weights

        # Define the complete model
        model = Sequential([
            Dense(256, activation='relu'),
            BatchNormalization(),
            Dense(128, activation='relu'),
            Dropout(0.5),
            BatchNormalization(),
            Dense(64, activation='relu'),
            Dropout(0.4),
            BatchNormalization(),
            Dense(1, activation='sigmoid')
        ])

        # Manually build the model to ensure all layers are constructed
        model.build((None, 224, 224, 3))
        model_path = 'models/best_model_weights.weights.h5'

        
        self.model = model.load_weights(model_path)

    
    def perform_object_detection(image, threshold=0.6, nms_threshold=0.4):
        ss = cv2.ximgproc.segmentation.createSelectiveSearchSegmentation()
        ss.setBaseImage(image)
        ss.switchToSelectiveSearchFast()
        rects = ss.process()
        
        car_boxes = []
        scores = []
        for x, y, w, h in rects:
            bounding_box = [x, y, x + w, y + h]  # Change to list format
            try:
                assert bounding_box[0] < bounding_box[2]
                assert bounding_box[1] < bounding_box[3]
                
                img_data = image[bounding_box[1]:bounding_box[3], bounding_box[0]:bounding_box[2]]
                img_data = cv2.resize(img_data, (224, 224))
                
                prediction = self.self.model.predict(img_data.reshape(1, 224, 224, 3))
                score = float(prediction.item())  # Convert prediction score to float
                if score > threshold:
                    car_boxes.append(bounding_box)
                    scores.append(score)
            except Exception as e:
                print('Error processing bounding box:', e)
        
        # Apply Non-Maximum Suppression
        indices = cv2.dnn.NMSBoxes(car_boxes, scores, threshold, nms_threshold)
        selected_boxes = [car_boxes[idx] for idx in indices.flatten()]
        
        return selected_boxes


    def draw_boxes(image, boxes):
        for box in boxes:
            x1, y1, x2, y2 = box  # Unpack the bounding box coordinates
            pt1 = (x1, y1)
            pt2 = (x2, y2)
            cv2.rectangle(image, pt1, pt2, (255, 0, 0), 2)
        
        return image

    def image_use(self, img_path):
        img = cv2.imread(img_path)
        car_boxes = perform_object_detection(img)
        image_with_boxes = draw_boxes(img.copy(), car_boxes)

        window_name = 'Labeled Image'

        # Create a named window
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, 850, 600)

        # Display the image in a window
        cv2.imshow(window_name, image_with_boxes)

        # Wait for a key press and close the window
        cv2.waitKey(0)
        cv2.destroyAllWindows()

