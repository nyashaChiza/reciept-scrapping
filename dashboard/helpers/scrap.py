import cv2
import imutils
import pytesseract
import numpy as np
from imutils.perspective import four_point_transform

class ReceiptScraper:
    def __init__(self, image_path, tesseract_path='C:/Program Files/Tesseract-OCR/tesseract.exe'):
        self.image_path = image_path
        self.receipt_text = ""
        
        # If Tesseract path is provided, set it
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path

    def load_image(self):
        # Load the image from the specified path
        img_orig = cv2.imread(self.image_path)
        if img_orig is None:
            raise Exception("Could not load image. Please check the path.")
        
        # Resize for easier processing, maintaining the original-to-resized ratio
        image = imutils.resize(img_orig, width=500)
        self.ratio = img_orig.shape[1] / float(image.shape[1])
        return img_orig, image

    def preprocess_image(self, image):
        if image is None :
            raise Exception("Input image for preprocessing is invalid.")
        
        # Convert the image to grayscale and apply Gaussian Blur
        # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        # edged = cv2.Canny(blurred, 75, 200)  # Edge detection
        return image

    def find_receipt_contour(self, edged):
        # Ensure the input image is a single-channel image
        if len(edged.shape) == 3:
            edged = cv2.cvtColor(edged, cv2.COLOR_BGR2GRAY)
        
        # Find contours in the edge map and sort them by size in descending order
        cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

        # Search for a four-point contour that may represent the receipt
        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(approx) == 4:
                return approx  # Found receipt contour
        return None

    def extract_receipt_text(self):
        # Load and preprocess the image
        img_orig, image = self.load_image()  # Unpack the tuple
        edged = self.preprocess_image(image)  # Use only the resized image for preprocessing

        # Find the receipt contour
        receiptCnt = self.find_receipt_contour(edged)
        if receiptCnt is None:
            raise Exception("Could not find receipt outline. Check edge detection settings.")

        # Apply a four-point transform to get a top-down view of the receipt
        try:
            receipt = four_point_transform(img_orig, receiptCnt.reshape(4, 2) * self.ratio)
        except Exception as e:
            raise Exception(f"Error during four-point transform: {e}")

        if receipt is None or receipt.size == 0:
            raise Exception("The four-point transformation did not return a valid image.")

        # Additional preprocessing for OCR (grayscale, denoising, thresholding)
        receipt_gray = cv2.cvtColor(receipt, cv2.COLOR_BGR2GRAY)
        if receipt_gray is None or receipt_gray.size == 0:
            raise Exception("Grayscale conversion failed on transformed receipt.")

        # Use a bilateral filter to reduce noise
        receipt_denoised = cv2.bilateralFilter(receipt_gray, 11, 17, 17)
        if receipt_denoised is None or receipt_denoised.size == 0:
            raise Exception("Denoising failed.")

        # Adaptive thresholding to make text stand out more
        receipt_thresh = cv2.adaptiveThreshold(receipt_denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        if receipt_thresh is None or receipt_thresh.size == 0:
            raise Exception("Thresholding failed.")

        # Perform OCR with updated configuration
        ocr_config = "--oem 3 --psm 4"  # You can also try --psm 11 if you have multi-column text
        self.receipt_text = pytesseract.image_to_string(receipt_thresh, config=ocr_config)

        # Optional: Save intermediate results for debugging
        cv2.imwrite("edged.jpg", edged)
        cv2.imwrite("transformed_receipt.jpg", receipt)
        cv2.imwrite("receipt_thresholded.jpg", receipt_thresh)

        return self.receipt_text

    def get_receipt_text(self):
        if not self.receipt_text:
            return "No text extracted. Please run extract_receipt_text() first."
        return self.receipt_text
