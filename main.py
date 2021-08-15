from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_pb2, status_code_pb2
import os
from glob import glob
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

channel = ClarifaiChannel.get_grpc_channel()
stub = service_pb2_grpc.V2Stub(channel)
metadata = (('authorization', 'Key 9daae19231d24425a64a2fb53493975a'),)
model_id = 'ushoe'
concepts = ['epic', 'nmd', 'presto', 'ultraboost']


def model(metadata):
    post_models_response = stub.PostModels(
        service_pb2.PostModelsRequest(
            models=[
                resources_pb2.Model(
                    id="ushoe",
                    output_info=resources_pb2.OutputInfo(
                        data=resources_pb2.Data(
                            concepts=[resources_pb2.Concept(id="epic", value=1),
                                    resources_pb2.Concept(id="nmd", value=1),
                                    resources_pb2.Concept(id="presto", value=1),
                                    resources_pb2.Concept(id="ultraboost", value=1)]
                        ),
                        output_config=resources_pb2.OutputConfig(
                            concepts_mutually_exclusive=False,
                            closed_environment=False
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )
    print(post_models_response)

    if post_models_response.status.code != status_code_pb2.SUCCESS:
        raise Exception("Post models failed, status: " + post_models_response.status.description)


def inputs(metadata):
    inputs = get_input(concepts)
    post_inputs_response = stub.PostInputs(
        service_pb2.PostInputsRequest(
            inputs=inputs
        ),
        metadata=metadata
    )

    if post_inputs_response.status.code != status_code_pb2.SUCCESS:
        for input_object in post_inputs_response.inputs:
            print("Input " + input_object.id + " status:")
            print(input_object.status)

        raise Exception("Post inputs failed, status: " + post_inputs_response.status.description)

    print(post_inputs_response)
        

def get_input(concepts):
    inputs = []
    for concept in concepts:
        file_paths = file_path('./training/' + concept + '/')
        for path in file_paths:
            with open(path, "rb") as f:
                file_bytes = f.read()
            if "epic" in path:
                concept=[
                    resources_pb2.Concept(id="epic", value=1),
                    resources_pb2.Concept(id="nmd", value=0),
                    resources_pb2.Concept(id="presto", value=0),
                    resources_pb2.Concept(id="ultraboost", value=0)
                ]
            elif "nmd" in path:
                concept=[
                    resources_pb2.Concept(id="nmd", value=1),
                    resources_pb2.Concept(id="epic", value=0),
                    resources_pb2.Concept(id="presto", value=0),
                    resources_pb2.Concept(id="ultraboost", value=0)
                ]
            elif "presto" in path:
                concept=[
                    resources_pb2.Concept(id="presto", value=1),
                    resources_pb2.Concept(id="epic", value=0),
                    resources_pb2.Concept(id="nmd", value=0),
                    resources_pb2.Concept(id="ultraboost", value=0)
                ]
            elif "ultraboost" in path:
                concept=[
                    resources_pb2.Concept(id="ultraboost", value=1),
                    resources_pb2.Concept(id="epic", value=0),
                    resources_pb2.Concept(id="nmd", value=0),
                    resources_pb2.Concept(id="presto", value=0)
                ]
            inputs.append(
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        image=resources_pb2.Image(
                            base64=file_bytes
                    ),
                        concepts=concept
                    )
                )
            )
    return inputs


def file_path(img_path):
    file_paths = []
    for file_path in glob(os.path.join(img_path, '*.png')):
        file_paths.append(file_path)

    return file_paths


def train(metadata):
    post_model_versions = stub.PostModelVersions(
        service_pb2.PostModelVersionsRequest(
            model_id="ushoe"
        ),
        metadata=metadata
    )

    print(post_model_versions)

    if post_model_versions.status.code != status_code_pb2.SUCCESS:
        raise Exception("Post model versions failed, status: " + post_model_versions.status.description)

    

def predict(metadata, url):
    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            model_id="ushoe",
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        image=resources_pb2.Image(
                            url=url
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )
    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)

    output = post_model_outputs_response.outputs[0].data
    return output



def nike_scraper():
    shoe_types = ['lifestyle', 'jordan', 'running', 'basketball', 'training-gym'
                  'soccer', 'skateboarding', 'football', 'baseball', 'golf', 'tennis',
                  'track-field', 'walking']
    mens_shoe_types = ['lifestyle', 'jordan', 'running', 'basketball', 'training-gym',
                       'soccer', 'skateboarding', 'football', 'baseball', 'golf', 'tennis',
                       'track-field', 'walking', 'sandals-slides']
    womens_shoe_types = ['lifestyle', 'running', 'basketball', 'soccer', 'training-gym',
                         'jordan', 'skateboarding', 'softball', 'golf', 'tennis', 'track-field',
                         'volleyball', 'cheerleading', 'walking', 'sandals-slides']
    unisex_shoe_types = ['lifestyle', 'running', 'basketball', 'training-gym',
                         'soccer', 'skateboarding', 'baseball', 'golf', 'track-field']
    genders = ['mens', 'womens', 'unisex']
    
    selected_types = ['lifestyle', 'running']
    selected_gender = 'mens'
    message = "Selected types unavailable for selected gender"
    if selected_gender == '':
        for shoe_type in selected_types:
            if not shoe_type in shoe_types:
                return message
        url = 'https://www.nike.com/w/new-shoes-3n82yzy7ok?sort=newest'
    if selected_gender == 'mens':
        for shoe_type in selected_types:
            if not shoe_type in mens_shoe_types:
                return message
        url = 'https://www.nike.com/w/new-mens-shoes-3n82yznik1zy7ok?sort=newest'
    elif selected_gender == 'womens':
        for shoe_type in selected_types:
            if not shoe_type in womens_shoe_types:
                return message
        url = 'https://www.nike.com/w/new-womens-shoes-3n82yz5e1x6zy7ok?sort=newest'
    elif selected_gender == 'unisex':
        for shoe_type in selected_types:
            if not shoe_type in unisex_shoe_types:
                return message
        url = 'https://www.nike.com/w/new-unisex-shoes-3n82yz3rauvzy7ok?sort=newest'
    else:
        return "Selected gender is invalid"
        
    images = []
    if len(selected_types) == 0:
        page = requests.get(url, headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.62'})
        soup = BeautifulSoup(page.content, 'html.parser')
        search = soup.find_all('a', class_='product-card__img-link-overlay')
        for result in search:
            links = {
                    "product_link": result['href'],
                    'img_link': result.div.div.noscript.img['src']
                }
            images.append(links)

    else:
        for style in selected_types:
            page = requests.get(url, headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.62'})
            soup = BeautifulSoup(page.content, 'html.parser')
            search = soup.find_all('a', class_='css-hrsjq4 css-xhk1pl css-1t2ydyg categories__item is--link')
            for result in search:
                if style in result['href']:
                    url = result['href']
                    break

            page = requests.get(url, headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.62'})
            soup = BeautifulSoup(page.content, 'html.parser')
            search = soup.find_all('a', class_='product-card__img-link-overlay')
            for result in search:
                links = {
                    "product_link": result['href'],
                    'img_link': result.div.div.noscript.img['src']
                }
                images.append(links)

    return images
            

def adidas_scraper():
    shoe_types = ['lifestyle', 'running', 'basketball', 'tennis', 'soccer',
                  'skateboarding', 'training', 'baseball', 'cycling']
    genders = ['men', 'women']

    selected_types = ['lifestyle', 'running']
    selected_gender = "men"
    urls = []
    for style in selected_types:
        url = 'https://www.adidas.com/us/' + selected_gender + '-' + style + '-athletic_sneakers-new_arrivals?sort=newest-to-oldest'
        urls.append(url)
    if len(urls) == 0:
        url = 'https://www.adidas.com/us/' + selected_gender + '-athletic_sneakers-new_arrivals?sort=newest-to-oldest'
        urls.append(url)
    
    images = []
    for url in urls:
        driver = webdriver.Chrome('./chromedriver')
        driver.get(url)
        ele = driver.find_element_by_tag_name('body')
        ele.send_keys(Keys.END)
        time.sleep(3)

        page = driver.page_source
        driver.close()

        soup = BeautifulSoup(page, 'html.parser')
        search = soup.find_all('div', class_='gl-product-card__assets')
        for result in search:
            links = {
                "product_link": result.a['href'],
                "img_link": result.a.img['src']
            }
            if 'https://' in links['img_link']:
                images.append(links)

    return images


def recs(metadata, images, brand):
    for img in images:
        sum = 0
        prediction = predict(metadata, img['img_link']).concepts
        for concept in prediction:
            sum = sum + concept.value
        if sum > 0.5:
            info = {
                "product_link": img['product_link'],
                "img_link": img['img_link'],
                "value": sum
            }
            brand.append(info)
    sort = sorted(brand, reverse=True, key= lambda k: k['value'])

    return sort[0:5]


def main(metadata):
    nike_images = nike_scraper()
    adidas_images = adidas_scraper()
    
    nike_list = []
    adidas_list = []
    
    nike = recs(metadata, nike_images, nike_list)
    adidas = recs(metadata, adidas_images, adidas_list)

    # TODO: email this stuff and rerun every week or so

main(metadata)