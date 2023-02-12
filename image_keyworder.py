from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
import os
def get_concepts(PAT, USER_ID, APP_ID, MODEL_ID, MODEL_VERSION_ID, IMAGE_FILE_LOCATION):
    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)

    metadata = (('authorization', 'Key ' + PAT),)

    userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

    with open(IMAGE_FILE_LOCATION, "rb") as f:
        file_bytes = f.read()

    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            user_app_id=userDataObject,  # The userDataObject is created in the overview and is required when using a PAT
            model_id=MODEL_ID,
            version_id=MODEL_VERSION_ID,  # This is optional. Defaults to the latest model version
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        image=resources_pb2.Image(
                            base64=file_bytes
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )
    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        print(post_model_outputs_response.status)
        raise Exception("Post model outputs failed, status: " + post_model_outputs_response.status.description)

    # Since we have one input, one output will exist here
    output = post_model_outputs_response.outputs[0]

    concepts = []
    for concept in output.data.concepts:
        concepts.append(concept.name)

    return concepts
path = "path"
for image in os.listdir(path):
    keywords = get_concepts("10b8f55d6c7d4eaf915be2c70fc1b4b7","xs512avo61rr","image_keyworder","general-image-recognition","aa7f35c01e0642fda5cf400f543e7c40",f"{path}\\{image}")
    os.rename(f"{path}\\{image}",f"{path}\\{str(keywords)}.jpg")
