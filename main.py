from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_pb2, status_code_pb2
import os
from glob import glob

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


"""
def nike_scraper():
    # Stuff


def adidas_scraper():
    # Stuff
"""
