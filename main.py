from flask import Flask, request, render_template
import cv2
import numpy as np
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def process_image(file_path):
    # Load the image
    A = cv2.imread(file_path)
    if A is None:
        return "Error: Image not loaded properly."
    
    # Convert to grayscale
    a = cv2.cvtColor(A, cv2.COLOR_BGR2GRAY)
    
    # Define ROIs with error handling for smaller images
    if a.shape[0] < 1200 or a.shape[1] < 1927:
        return "Currency is fake"

    a2tr = a[330:1200, 1016:1927]
    a2_str = a[5:1100, 2080:2151]
    
    # Convert to HSV
    hsvImageReal = cv2.cvtColor(A, cv2.COLOR_BGR2HSV)
    croppedImageReal = hsvImageReal[5:1100, 2080:2151]
    
    # Thresholding
    satThresh = 0.3
    valThresh = 0.9
    g = croppedImageReal[:,:,1] > satThresh
    h = croppedImageReal[:,:,2] < valThresh
    BWImageReal = g & h

    # Morphological operations
    if a2_str.size == 0:
        return "Currency is fake"
    binr = cv2.threshold(a2_str, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    kernel = np.ones((3, 3), np.uint8)
    invert = cv2.bitwise_not(binr)
    if invert.size == 0:
        return "Currency is fake"
    BWImageCloseReal = cv2.morphologyEx(invert, cv2.MORPH_GRADIENT, kernel)

    # Area open function
    def bwareaopen(img, min_size, connectivity=8):
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(img, connectivity=connectivity)
        for i in range(num_labels):
            label_size = stats[i, cv2.CC_STAT_AREA]
            if label_size < min_size:
                img[labels == i] = 0
        return img

    areaopenReal = bwareaopen(BWImageCloseReal, 15)
    bw = areaopenReal
    labels = np.zeros(bw.shape)
    countReal = cv2.connectedComponentsWithStats(bw, labels, 8)

    # Check currency legitimacy
    if countReal[0] > 1:  # Assuming more than 1 connected component indicates legitimacy
        return "Currency is legitimate"
    else:
        return "Currency is fake"

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            result = process_image(file_path)
            return render_template('result.html', result=result)
    return render_template('index.html')

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
