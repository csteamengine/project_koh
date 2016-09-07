#!/usr/bin/env python3

# Import the required modules
import cv2, os
import numpy as np
from PIL import Image

# For face detection we will use the Haar Cascade provided by OpenCV.
cascade_path = "/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml"

# Default max number of images for a given student.
# Every time a student is re-identified, it will store an image on
# the server up to the maxImages amount.
default_max_images = 20


def main():
    # TODO
    print("Initializing Koh...")
    koh = KohFaceRecognizer()
    koh.train_existing_faces("../uploads")



class KohFaceRecognizer:
    def __init__(self):
        # For face detection
        self.faceCascade = cv2.CascadeClassifier(cascade_path)

        # For face recognition
        self.recognizer = cv2.face.createLBPHFaceRecognizer()

    def detect_faces(self, img_path):
        """
        Detects multiple faces in an image and stores them in an
        array of tuples named `faces_in_image`. The tuples have the
        x, y, width, and height of the bounding box surrounding
        the face. Also creates a uint8 numpy array out of the given
        image called `prediction_image` after it's been converted to
        greyscale.

        :param img_path: The path of the image you want faces detected in.
        :return: (prediction_image, faces_in_image)
        """
        """

        """
        greyscale_image = Image.open(img_path).convert('L')
        prediction_image = np.array(greyscale_image, 'uint8')
        faces_in_image = self.faceCascade.detectMultiScale(prediction_image)
        return prediction_image, faces_in_image

    def train_new_face(self, student_id, img_path):
        # TODO
        print("train_new_face({}, {})".format(student_id, img_path))

    def train_existing_faces(self, dir_path):
        """
        Trains the recognizer with faces from the given directory path.
        The directory path should be formatted as follows:
        dir_path/
        ----student<student_id>/
        --------

        :param dir_path: The path to the directory containing face images.
        :return:
        """
        # Call the get_images_and_labels function and get the face images and the
        # corresponding labels
        images, student_ids = get_images_and_ids(dir_path)
        cv2.destroyAllWindows()

        # Perform the tranining
        self.recognizer.train(images, np.array(student_ids))

    # Returns an array of PredictionResult objects
    def predict_face(self, img_path):
        prediction_image, faces_in_image = self.detect_faces(img_path)
        prediction_results = []
        for (x, y, w, h) in faces_in_image:
            result = cv2.face.MinDistancePredictCollector()
            self.recognizer.predict(prediction_image[y: y + h, x: x + w], result, 0)
            student_id_predicted = result.getLabel()
            prediction_confidence = result.getDist()
            prediction_results.append(PredictionResult(
                img_path, prediction_image[y: y + h, x: x + w], student_id_predicted, prediction_confidence))
        return prediction_results


class Student:
    def __init__(self, student_id):
        self.student_id = student_id


class PredictionResult:
    def __init__(self, img_path, img_region, student_id, confidence):
        self.img_path = img_path
        self.img_region = img_region
        self.student_id = student_id
        self.confidence = confidence


if __name__ == "__main__": main()



def get_images_and_ids(path):
    # Append all the absolute image paths in a list image_paths
    # We will not read the image with the .sad extension in the training set
    # Rather, we will use them to test our accuracy of the training
    image_paths = [os.path.join(path, f) for f in os.listdir(path) if not f.endswith('.sad')]
    # images will contains face images
    images = []
    # labels will contains the label that is assigned to the image
    labels = []
    for image_path in image_paths:
        # Read the image and convert to grayscale
        image_pil = Image.open(image_path).convert('L')
        # Convert the image format into numpy array
        image = np.array(image_pil, 'uint8')
        # Get the label of the image
        nbr = int(os.path.split(image_path)[1].split(".")[0].replace("subject", ""))
        # Detect the face in the image
        faces = faceCascade.detectMultiScale(image)
        # If face is detected, append the face to images and the label to labels
        for (x, y, w, h) in faces:
            images.append(image[y: y + h, x: x + w])
            labels.append(nbr)
            cv2.imshow("Adding faces to traning set...", image[y: y + h, x: x + w])
            cv2.waitKey(50)
    # return the images list and labels list
    return images, labels


# Append the images with the extension .sad into image_paths
#image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.sad')]
# nbr_actual = int(os.path.split(img_path)[1].split(".")[0].replace("subject", ""))
