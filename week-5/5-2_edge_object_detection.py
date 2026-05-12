
import cv2
import numpy as np
try:
    from tflite_runtime.interpreter import Interpreter
except ImportError:
    from tensorflow.lite.python.interpreter import Interpreter

def run_inference(model_path, image_path, threshold=0.5):
    # Load the TFLite model and allocate tensors.
    interpreter = Interpreter(model_path=model_path)
    interpreter.allocate_tensors()

    # Get input and output details.
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Prepare image
    img = cv2.imread(image_path)
    h, w, _ = img.shape
    input_shape = input_details[0]['shape']
    input_data = cv2.resize(img, (input_shape[1], input_shape[2]))
    input_data = np.expand_dims(input_data, axis=0)

    # Run inference
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    # Retrieve detection results
    # (Indexes vary by model export version, standard Azure Custom Vision export used here)
    boxes = interpreter.get_tensor(output_details[0]['index'])[0] # Bounding box coordinates
    classes = interpreter.get_tensor(output_details[1]['index'])[0] # Class index
    scores = interpreter.get_tensor(output_details[2]['index'])[0] # Confidence score

    for i in range(len(scores)):
        if scores[i] > threshold:
            ymin, xmin, ymax, xmax = boxes[i]
            # Convert normalized coordinates back to pixel values
            (left, right, top, bottom) = (xmin * w, xmax * w, ymin * h, ymax * h)
            cv2.rectangle(img, (int(left), int(top)), (int(right), int(bottom)), (0, 255, 0), 2)
            print(f"Detected Object {int(classes[i])} with confidence {scores[i]:.2f}")

    cv2.imwrite('detection_result.jpg', img)
    print("Result saved as detection_result.jpg")

if __name__ == "__main__":
    # Example usage: python edge_object_detection.py
    # run_inference('model.tflite', 'test_citrus.jpg')
    pass
