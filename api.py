from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import time
from districtfinderapp import DistrictFinder
from imageclassifierapp import ImageClassifier

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)

distFinder = DistrictFinder()
imageClassifier = ImageClassifier()

@app.get('/districtfinder')
def district_finder(address_str):
    return distFinder.get_result_json(address_str)

@app.post('/imageclassifier/upload_image')
def upload_image(file: UploadFile = File(...)):
    return imageClassifier.upload_image(file)