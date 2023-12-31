from fastapi import APIRouter

from app.utils.utils import base64ToVideo, remove_video_file
from app.services.skeleton_extraction_service import extract_skeleton
from app.services.video_adjustment_service import check_video_resolution, rescale_to_720x720, crop_and_resize_to_720x720
from app.utils.async_utils import get_resource

from app.dto.base64video_req_dto import Base64Video
from app.dto.json_req_dto import JsonLandmark
from app.dto.prediction_res_dto import Prediction


prediction_router = APIRouter(
    tags=["predict"],
    responses={404: {"description": "Not found"}},
)

@prediction_router.post("/video", response_model=Prediction)
def upload(video: Base64Video):
    # Convert base64 to mp4
    fileName = base64ToVideo(video.data)

    if(not fileName):
        return Prediction(**{"prediction": "", "message": "Invalid file"})
    
    # If the video file is not in 720x720, change it
    status = check_video_resolution(fileName)
    
    if(status == 1):
        fileName = rescale_to_720x720(fileName)
    elif(status == 2):
        fileName = crop_and_resize_to_720x720(fileName)
    elif(status == 3):
        remove_video_file(fileName)
        return Prediction(**{"prediction": "", "message": "Could not change resolation"})
    
    # Extract skeleton
    x, y = extract_skeleton(fileName)
    print(x.shape, y.shape)

    # Preprocess
    x, y = get_resource('lstm_model').preprocess_video_landmarks(x, y)

    # Predict sign
    predicted_class = get_resource('lstm_model').predict(x, y)

    remove_video_file(fileName)

    if(not predicted_class):  
        return Prediction(**{"prediction": "", "message": "Could not predict sign"})

    
    return Prediction(**{"prediction": predicted_class, "message": "Success"})


@prediction_router.post("/text", response_model=Prediction)
def upload(landmarkObj: JsonLandmark):

    # Extract x and y
    x, y, err = get_resource('lstm_model').json_to_numpy(landmarkObj)

    if(err):
        return Prediction(**{"prediction": "", "message": "Invalid landmarks object"})

    # Preprocess
    x, y = get_resource('lstm_model').preprocess_text_landmarks(x, y)

    # Predict sign
    predicted_class = get_resource('lstm_model').predict(x, y)

    if(not predicted_class):  
        return Prediction(**{"prediction": "", "message": "Could not predict sign"})

    
    return Prediction(**{"prediction": predicted_class, "message": "Success"})