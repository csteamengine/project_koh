#!/usr/bin/env python3

# Import the required modules
import cv2, os, scipy.misc
import numpy as np
from PIL import Image

# For face detection we will use the Haar Cascade provided by OpenCV.
cascade_path = "/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml"

# Default max number of images for a given student.
# Every time a student is re-identified, it will store an image on
# the server up to the maxImages amount.
default_max_images = 20    # TODO: Haven't used this yet, but we'll want to somehow limit
                           # how many images are saved to the server for any given student.

# The directory path for all saved faces
saved_faces_path = "../saved_faces"

# Determines filename convention for image sequence number in student<id>.<sequence_number>.jpg
# Ex: Padding of 3 gives "studentXYZ.001.jpg"; padding of 4 gives "studentXYZ.0001.jpg", etc.
saved_image_sequence_padding = 3


def main():
    print("Starting sample app.")

    # Initialize and train it with existing faces
    koh = KohFaceRecognizer()
    saved_faces_path = "../test/yalefaces"
    koh.train_existing_faces(saved_faces_path)

    # For this sample app, we'll test all the images in the yalefaces-sad folder
    # against the other images that have already been trained in.
    sad_faces_path = "../test/yalefaces-sad"
    sad_faces = [os.path.join(sad_faces_path, f) for f in os.listdir(sad_faces_path)]
    print("Printing the results:\n")
    for face in sad_faces:
        results = koh.predict_face(face)
        for result in results:
            print("FILE:\n  {}\nPREDICTION:\n  numpy_image: (not shown)\n  student_id: {}\n  confidence: {}\n"
                  .format(face, result.student_id, result.confidence))
            # If we are happy with the result, we'll typically do the following:
            # Train the recognizer with the new face.
            koh.train_new_face(result.student_id, result.numpy_image)

            # Save the face snapshot to the server (which we won't do in this sample app):
            # new_image_path = koh_api.save_prediction_result_image(result)


class KohFaceRecognizer:
    def __init__(self):
        print("Initializing KohFaceRecognizer.")
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
        greyscale_image = Image.open(img_path).convert('L')
        prediction_image = np.array(greyscale_image, 'uint8')
        faces_in_image = self.faceCascade.detectMultiScale(prediction_image)
        return prediction_image, faces_in_image

    def save_prediction_result_image(self, prediction_result):
        """
        Saves the numpy_image and student_id number from the PredictionResult
        to a jpg file of the format 'student<id>.<image_sequence_number>.jpg'
        and returns the path to the new file.

        :param prediction_result:
        :return: The path to the file that was saved.
        """
        return self.save_student_image(prediction_result.numpy_image, prediction_result.student_id)

    def save_student_image(self, numpy_image, student_id):
        """
        Saves the params to a jpg file of the format 'student<id>.<image_sequence_number>.jpg'
        and returns the path to the new file.

        :param numpy_image:
        :param student_id:
        :return: The path to the file that was saved.
        """
        # Get existing filenames for this student
        existing_image_filenames = [f for f in os.listdir(saved_faces_path) if f.startswith("student{}.".format(student_id))]
        # Next we'll parse the image sequence numbers out of the filenames
        existing_image_numbers = []
        for path in existing_image_filenames:
            try:
                n = int(path.split(".")[1])
                existing_image_numbers.append(n)
            except ValueError:
                print("The saved face file {} was skipped because it wasn't in the right format.".format(path))
                continue
        # Get the max number, and add 1 for the new image number
        new_image_number = max(existing_image_numbers, default=-1) + 1
        # Format the number as a string with zeros for padding
        number_string = format(new_image_number, "0{}".format(saved_image_sequence_padding))
        # Save the file
        filename = "student{}.{}.jpg".format(student_id, number_string)
        file_path = "{}/{}".format(saved_faces_path, filename)
        scipy.misc.toimage(numpy_image, cmin=0.0, cmax=...).save(file_path)
        return file_path

    def train_new_face(self, student_id, numpy_image):
        """
        Used to train the recognizer with a new face. You get numpy_images back
        in an array after calling `detect_faces()`. Use one of the items from
        the `faces_in_image` array that gets returned from that method.

        :param student_id:
        :param numpy_image:
        :return:
        """
        self.recognizer.train([numpy_image], np.array([student_id]))

    def train_new_faces(self, student_id_array, numpy_image_array):
        self.recognizer.train(numpy_image_array, np.array(student_id_array))

    def train_existing_faces(self, dir_path):
        """
        Trains the recognizer with faces from the given directory path.
        The directory path should be formatted as follows:
        dir_path/
        |-- student<student1_id>.000.jpg
        |-- student<student1_id>.001.jpg
        |-- student<student1_id>.002.jpg
        |-- student<student2_id>.000.jpg
        |-- student<student2_id>.001.jpg
        ...

        :param dir_path: The path to the directory containing face images.
        :return:
        """
        print("Training existing faces into the recognizer...", end="", flush=True)
        # Append all the absolute image paths in a list image_paths
        image_filenames = [f for f in os.listdir(dir_path)]
        images = []
        student_ids = []
        for filename in image_filenames:
            id_ = int(filename.split(".")[0].replace("student", ""))
            image_path = os.path.join(dir_path, filename)
            prediction_image, faces_in_image = self.detect_faces(image_path)
            # If face is detected, append the face to images and the label to labels
            for (x, y, w, h) in faces_in_image:
                images.append(prediction_image[y: y + h, x: x + w])
                student_ids.append(id_)
        self.recognizer.train(images, np.array(student_ids))
        print("done.")

    def predict_face(self, img_path):
        """
        Tries to recognize (predict) the face(s) in the image, returning an
        array of PredictionResult objects upon completion.

        :param img_path: The path to the image.
        :return: An array of PredictionResult objects.
        """
        prediction_image, faces_in_image = self.detect_faces(img_path)
        prediction_results = []
        for (x, y, w, h) in faces_in_image:
            result = cv2.face.MinDistancePredictCollector()
            self.recognizer.predict(prediction_image[y: y + h, x: x + w], result, 0)
            student_id_predicted = result.getLabel()
            prediction_confidence = result.getDist()
            prediction_results.append(PredictionResult(
                prediction_image[y: y + h, x: x + w], student_id_predicted, prediction_confidence))
        return prediction_results


class PredictionResult:
    def __init__(self, numpy_image, student_id, confidence):
        self.numpy_image = numpy_image
        self.student_id = student_id
        # The lower the confidence number, the more likely it's a match
        self.confidence = confidence


if __name__ == "__main__":
    main()
