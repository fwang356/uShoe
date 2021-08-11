from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
import os
from glob import glob

app = ClarifaiApp(api_key='8901c8184bf9496996607fd323282045')
model_id = 'ushoe'
concepts = ['epic', 'presto', 'ultraboost']


def model():
    model = app.models.create(model_id, concepts=concepts)
    model = app.model.get(model_id)
    model.train()
    

def images(concepts):
    for concept in concepts:
        images = create_image_set('./training/' + concept + '/', concepts=[concept])
        app.inputs.bulk_create_images(images)


def create_image_set(img_path, concepts):
    images = []
    for file_path in glob(os.path.join(img_path, '*.png')):
        img = ClImage(filename=file_path, concepts=concepts)
        images.append(img)

    return images


def predict(image_url):
    model = app.models.get(model_id)
    prediction = model.predict_by_url(image_url)
    results = prediction['outputs'][0]['data']['concepts']
    return results


def nike_scraper():
    # Stuff


def adidas_scraper():
    # Stuff