# OCR-Project-Read-code
This project implements an OCR (Optical Character Recognition) system capable of extracting text from screenshots of code editors, even when using Dark Mode.  The goal is to automate the reading of code or text captured in images, addressing common issues with screenshots, such as:  Incorrect rotation caused by smartphone EXIF metadata .



OCR for Dark Mode Screenshots

Overview

This project provides a robust solution for extracting text from screenshots taken in dark mode (e.g., Acode, VSCode). It uses Python, Tesseract OCR, and OpenCV to preprocess images and accurately extract text while handling common issues like dark backgrounds and incorrect EXIF orientation.


---

Features

Automatic Dark Mode Detection: Detects whether a screenshot uses dark mode and inverts colors for better OCR results.

EXIF Orientation Correction: Automatically corrects image rotation based on EXIF data.

Advanced Preprocessing: Converts images to grayscale and applies adaptive thresholding for improved OCR accuracy.

Multiple OCR Configurations: Tries different Tesseract configurations to extract the best possible text, including code snippets.

Text Cleaning: Removes unwanted characters (|, :) and preserves line breaks for readable output.

Result Scoring: Automatically chooses the best OCR result based on code-like patterns and structure.

Downloadable Output: Saves extracted text to a .txt file with timestamp and statistics.



---

Installation

Make sure you have Python 3 installed. Required libraries:

pip install pillow opencv-python pytesseract


---

Usage

1. Run the script in a Python environment (e.g., Google Colab, Jupyter Notebook).


2. Upload your screenshot when prompted.


3. The script will:

Detect dark mode and invert colors if needed.

Preprocess the image.

Run Tesseract OCR with multiple configurations.

Clean the extracted text and select the best result.



4. The final text will be displayed and saved as a .txt file for download.




---

Example

Input: A dark mode screenshot from Acode.
Output: Extracted text ready for coding or documentation purposes.


---

Future Improvements

Extend support to multiple languages and fonts.

Integrate directly with code editors for automatic text extraction.

Implement batch processing for multiple screenshots at once.



---

License

This project is licensed under the MIT License.


---
