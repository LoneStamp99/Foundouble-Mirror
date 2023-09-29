import os
import argparse
import collections
import cv2
import numpy as np
import imagehash
from PIL import Image

class ImgDuplicateDetector:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.images = []
        self.MSE_THRESH = 10
        self.HASH_THRESH = 10

    def scan_filesystem(self):
        for dirpath, _, filenames in os.walk(self.root_dir):
            for filename in filenames:
                if os.path.splitext(filename)[1] not in ['.jpg', '.jpeg', '.png', '.bmp']:
                    continue
                file_path = os.path.join(dirpath, filename)
                try:
                    img = cv2.imread(file_path)
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    self.images.append((file_path, img))
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    def compare_images(self, img1, img2):
        mse = np.sum((img1.astype("float") - img2.astype("float")) ** 2)
        mse /= float(img1.shape[0] * img1.shape[1])
        return mse

    def detect_duplicates(self):
        duplicates = {}
        hashes = collections.defaultdict(list)
        for i, (file_path, img1) in enumerate(self.images):
            img2 = Image.fromarray(img1)
            hash1 = str(imagehash.phash(img2))
            hashes[hash1].append(i)

        for idx1, (file_path1, img1) in enumerate(self.images):
            img2 = Image.fromarray(img1)
            hash1 = str(imagehash.phash(img2))
            if hash1 in duplicates:
                continue
            for idx2 in hashes[hash1]:
                if idx1 == idx2:
                    continue
                file_path2, img2 = self.images[idx2]
                mse = self.compare_images(img1, img2)
                if mse < self.MSE_THRESH:
                    duplicates[idx1] = [file_path1, file_path2]
                    break

        return duplicates

    def delete_image(self, image_path):
        try:
            os.remove(image_path)
            print("Image deleted:", image_path)
        except Exception as e:
            print("Error deleting image:", e)

def parse_args():
    parser = argparse.ArgumentParser(description='Detect and delete duplicate images in file system.')
    parser.add_argument('root_dir', metavar='DIR', type=str, help='root directory to scan')
    return parser.parse_args()

def main():
    args = parse_args()
    detector = ImgDuplicateDetector(args.root_dir)
    detector.scan_filesystem()
    duplicates = detector.detect_duplicates()

    if len(duplicates) == 0:
        print("No duplicate images found.")
        return

    print("Found duplicate images:")
    for i, (idx1, files) in enumerate(duplicates.items()):
        idx2 = idx1 + 1
        print(f"{i+1}. {files[0]}")
        print(f"   {idx1+1}. {files[1]}")
        print(f"   {idx2+1}. {files[2]}")
    selected_dup = input("Select duplicate to delete (0 to exit): ")
    try:
        selected_dup = int(selected_dup)
        if selected_dup <= 0:
            return
        idx1 = (selected_dup-1) * 2
        idx2 = idx1 + 1
        file_path1 = duplicates[idx1][0]
        file_path2 = duplicates[idx2][0]
        for i, (idx, files) in enumerate(duplicates.items()):
            if idx == idx1 or idx == idx2:
                detector.delete_image(files[0])
    except (ValueError, IndexError):
        print("Invalid input. Exiting...")

if __name__ == "__main__":
    main()
