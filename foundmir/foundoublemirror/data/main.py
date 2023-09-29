import os
import platform
import time
from tkinter import Tk, filedialog
import easygui as eg
import shutil
import tensorflow as tf
import tensorflow_hub as hub
import subprocess
import cv2
from PIL import Image, ExifTags # import these two modules for image rotation
import numpy as np # import numpy for manipulating image arrays

subprocess.call(["python", "./banner.py"])

class ImgDuplicateDetector:
    """
    Class to detect duplicate images in a folder.
    """

    def __init__(self, folder_path):
        """
        Initialize the ImgDuplicateDetector object with the folder path.
        """
        self.folder_path = folder_path
        self.image_list = {}
        self.duplicates = []

    def scan_filesystem(self, scan_limit=None):
        """
        Scan the folder and create a dictionary with image files and their corresponding hashes.
        """
        total_images = 0
        system_images = 0
        start_time = time.time()
        if scan_limit:
            for dirpath, dirnames, filenames in os.walk(scan_limit):
                for filename in filenames:
                    if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
                        file_path = os.path.join(dirpath, filename)
                        total_images += 1
                        try:
                            with open(file_path, 'rb') as f:
                                image_bytes = f.read()
                                self.image_list[file_path] = hash(image_bytes)
                        except:
                            system_images += 1
                        elapsed_time = time.time() - start_time
                        print(f"Total images scanned: {total_images} | Elapsed time: {elapsed_time:.2f}s | Scanning: {file_path}", end="\r")
        else:
            if platform.system() == 'Windows':
                for drive in ['C:', 'D:', 'E:', 'F:', 'G:', 'H:', 'I:', 'J:', 'K:', 'L:', 'M:', 'N:', 'O:', 'P:', 'Q:', 'R:', 'S:', 'T:', 'U:', 'V:', 'W:', 'X:', 'Y:', 'Z:']:
                    for dirpath, dirnames, filenames in os.walk(drive):
                        for filename in filenames:
                            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
                                file_path = os.path.join(dirpath, filename)
                                total_images += 1
                                if os.path.islink(file_path) or 'AppData' in file_path:
                                    system_images += 1
                                    continue
                                try:
                                    # Rotate image based on EXIF tags
                                    img = Image.open(file_path)
                                    for orientation in ExifTags.TAGS.keys():
                                        if ExifTags.TAGS[orientation]=='Orientation':
                                            break
                                    exif=dict(img._getexif().items())

                                    if exif[orientation] == 3:
                                        img=img.rotate(180, expand=True)
                                    elif exif[orientation] == 6:
                                        img=img.rotate(270, expand=True)
                                    elif exif[orientation] == 8:
                                        img=img.rotate(90, expand=True)

                                    img.save(file_path)

                                    # Hash image
                                    with open(file_path, 'rb') as f:
                                        image_bytes = f.read()
                                        self.image_list[file_path] = hash(image_bytes)
                                except:
                                    system_images += 1
                                elapsed_time = time.time() - start_time
                                print(f"Total images scanned: {total_images} | Elapsed time: {elapsed_time:.2f}s | Scanning: {file_path}", end="\r")
            elif platform.system() in ['Linux', 'Darwin']:
                for dirpath, dirnames, filenames in os.walk('/'):
                    for filename in filenames:
                        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
                            file_path = os.path.join(dirpath, filename)
                            total_images += 1
                            if os.path.islink(file_path):
                                system_images += 1
                                continue
                            try:
                                # Rotate image based on EXIF tags
                                img = Image.open(file_path)
                                for orientation in ExifTags.TAGS.keys():
                                    if ExifTags.TAGS[orientation]=='Orientation':
                                        break
                                exif=dict(img._getexif().items())

                                if exif[orientation] == 3:
                                    img=img.rotate(180, expand=True)
                                elif exif[orientation] == 6:
                                    img=img.rotate(270, expand=True)
                                elif exif[orientation] == 8:
                                    img=img.rotate(90, expand=True)

                                img.save(file_path)

                                # Hash image
                                with open(file_path, 'rb') as f:
                                    image_bytes = f.read()
                                    self.image_list[file_path] = hash(image_bytes)
                            except:
                                system_images += 1
                            elapsed_time = time.time() - start_time
                            print(f"Total images scanned: {total_images} | Elapsed time: {elapsed_time:.2f}s | Scanning: {file_path}", end="\r")

        self.total_images = total_images
        self.system_images = system_images
        print(f"\nScan complete | Total images scanned: {self.total_images} | System images skipped: {self.system_images} | Scanned path: {self.folder_path}")

    def detect_duplicates(self, threshold=0.95):
        """
        Compare the hashes of the images in the dictionary and store duplicate image paths in the self.duplicates list.
        """
        for file_path, hash_value in self.image_list.items():
            is_duplicate = False
            for i, duplicates in enumerate(self.duplicates):
                if self.compare_images(file_path, duplicates[0], threshold):
                    duplicates.append(file_path)
                    is_duplicate = True
                    break
            if not is_duplicate:
                self.duplicates.append([file_path])

    def report_duplicates(self, model):
        """
        Generate a prompt for found duplicate images
        """
        if len(self.duplicates) > 0:
            print(f"Found {len(self.duplicates)} sets of duplicate images:")
            for i, file_group in enumerate(self.duplicates):
                print(f"Duplicate set {i+1} ({len(file_group)} images):")
                for file_path in file_group:
                    print(f" - {file_path}")
                    # Generate image classification labels
                    labels = classify_image(file_path, model, batch_size=1)
                    print(f"   Labels: {labels}")
                print()

            while True:
                action = input("Enter 'd' to delete a specific duplicate image, 'c' to copy to a new folder, or 's' to skip: ")
                if action.lower() == 'd':
                    while True:
                        file_path = input("Enter the image path you want to delete: ")
                        if file_path in self.image_list:
                            os.remove(file_path)
                            
                            for i, file_group in enumerate(self.duplicates):
                                if file_path in file_group:
                                    file_group.remove(file_path)
                                    print(f"Removed {file_path} from duplicate set {i+1}")
                                    
                            self.duplicates = [l for l in self.duplicates if l] # Remove empty lists
                            print(f"Deleted image: {file_path}")
                            break
                        else:
                            print(f"Could not find image: {file_path}")
                elif action.lower() == 'c':
                    self.copy_duplicates()
                    break
                elif action.lower() == 's':
                    break
                else:
                    print("Invalid input. Try again.")

    def delete_duplicates(self):
        """
        Delete duplicate images.
        """
        for file_group in self.duplicates:
            for file_path in file_group:
                os.remove(file_path)
                print(f"Deleted image: {file_path}")
        self.duplicates = []

    def copy_duplicates(self):
        """
        Copy duplicate images to a new folder.
        """
        folder = filedialog.askdirectory(title="Select folder to copy duplicate images to")
        if not folder:
            print("Invalid folder path. Try again.")
            return
        output_folder = os.path.join(folder, "theDuplicate")
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)
        for file_group in self.duplicates:
            for file_path in file_group:
                file_name = os.path.basename(file_path)
                output_file = os.path.join(output_folder, file_name)
                shutil.copy2(file_path, output_file)
                print(f"Copied image: {file_path} -> {output_file}")
        self.duplicates = []


    def compare_images(self, file_path1, file_path2, threshold):
        """
        Compare the hashes of two images and return a boolean indicating whether they are similar (i.e., duplicates).
        """
        hash1 = self.image_list[file_path1]
        hash2 = self.image_list[file_path2]
        if hash1 == hash2:
            return True
        else:
            # Compute the Hamming distance between the hashes
            hamming_distance = bin(hash1 ^ hash2).count('1')
            similarity = 1 - (hamming_distance / 64)
            return similarity >= threshold


def classify_image(image_path, model, batch_size=1):
    """
    Classify the image at the given path using the given model and return the top 5 predicted labels.
    """
    img = cv2.imread(image_path)
    img = cv2.resize(img, (224, 224))
    img = tf.keras.applications.mobilenet_v2.preprocess_input(img)
    batch = np.zeros((batch_size, 224, 224, 3), dtype=np.float32)
    batch[0] = img
    predictions = model.predict(batch)
    predictions = predictions[:, :1000]  # Add this line to select the required output tensor
    top_k = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=5)
    return top_k[0]


def main():
    # Load the pre-trained model outside of the main function
    model = tf.keras.Sequential([
        hub.KerasLayer("https://tfhub.dev/google/imagenet/mobilenet_v2_100_224/feature_vector/4",
                       output_shape=[1000],
                       trainable=False)
    ])

    while True:
        print("Select one of the following options:")
        print("1. Scan now")
        print("2. Add image folder")
        print("3. Exit")

        user_input = input("Selection: ")

        if user_input == '3':
            break
        elif user_input == '1':
            detector = ImgDuplicateDetector(os.getcwd())
            detector.scan_filesystem()
            detector.detect_duplicates()
            detector.report_duplicates(model)

        elif user_input == '2':
            root = Tk()
            root.withdraw()
            folder_path = filedialog.askdirectory()

            if not folder_path:
                print("Invalid folder path. Try again.")
                continue

            detector = ImgDuplicateDetector(folder_path)
            detector.scan_filesystem(scan_limit=folder_path)
            detector.detect_duplicates()
            detector.report_duplicates(model)

        else:
            print("Invalid input. Try again.")


if __name__ == "__main__":
    main()
