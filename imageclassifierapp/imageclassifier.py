import os
import shutil
from werkzeug.utils import secure_filename
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.applications.vgg16 import decode_predictions
from tensorflow.keras.applications.vgg16 import VGG16
from pathlib import Path

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

class ImageClassifier:
    def __init__(self):
        self._upload_folder = './uploads/'

    def _allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def save_upload_file(self, file, destination):
        try:
            with destination.open("wb") as buffer:
                shutil.copyfileobj(file, buffer)
        finally:
            file.close()

    def upload_image(self, file):
        if file.filename == '':
            return 'Add a file'

        if file and self._allowed_file(file.filename):
            filename = secure_filename(file.filename)
            self.save_upload_file(file.file, Path(os.path.join(self._upload_folder, file.filename)))
            label, acc = self._getPrediction(filename)
            output = {}
            output['label'] = label
            output['accuracy'] = acc
            return output
        else:
            return 'Incorrect format'

    def _getPrediction(self, filename):
        model = VGG16()
        image = load_img(self._upload_folder + filename, target_size=(224, 224))
        image = img_to_array(image)
        image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
        image = preprocess_input(image)
        yhat = model.predict(image)
        label = decode_predictions(yhat)
        label = label[0][0]
        print('%s (%.2f%%)' % (label[1], label[2] * 100))
        return label[1].capitalize(), "{:.2f}".format(label[2] * 100)
