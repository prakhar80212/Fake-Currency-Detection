# Fake-Currency-Detection

This project demonstrates a web application for detecting fake currency using image processing techniques in OpenCV. The system analyzes uploaded currency images to determine their legitimacy.

Features
Upload an image of currency for verification
Image processing using OpenCV to analyze currency features
Returns a result indicating whether the currency is legitimate or fake
Simple web interface for user interaction
Technologies Used
Python
Flask
OpenCV
NumPy

Installation
Clone the repository:

bash
git clone https://github.com/your-repository/fake-currency-detection.git
cd fake-currency-detection
Set up a virtual environment and install dependencies:

bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

bash
mkdir uploads
Run the Flask application:

bash
python app.py
Open your browser and navigate to http://127.0.0.1:5000/.

Upload an image of currency to verify its legitimacy.

Files
app.py: Main application file
templates/index.html: HTML template for the upload interface
templates/result.html: HTML template to display the result
uploads/: Directory to store uploaded images

How It Works
Image Upload: User uploads an image of the currency.
Image Processing:
Loads the image and converts it to grayscale.
Defines Regions of Interest (ROIs) and converts the image to HSV.
Applies thresholding and morphological operations to detect features.
Uses connected component analysis to determine the currency's legitimacy.
Result Display: The application returns a result indicating whether the currency is legitimate or fake based on the analysis.

Acknowledgments
OpenCV for providing tools for image processing tasks.
Flask for the web framework.
