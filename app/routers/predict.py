from fastapi import APIRouter

from app.utils.utils import base64ToVideo, remove_video_file
from app.services.skeleton_extraction import extract_skeleton
from app.services.video_adjustment import check_video_resolution, convert_to_720x720
from app.utils.async_utils import get_resource

from app.dto.base64video_req_dto import Base64Video
from app.dto.json_req_dto import JsonLandmark
from app.dto.prediction_res_dto import Prediction


router = APIRouter(
    tags=["predict"],
    responses={404: {"description": "Not found"}},
)

@router.post("/video", response_model=Prediction)
def upload(video: Base64Video):
    # Convert base64 to mp4
    fileName = base64ToVideo(video.data)

    if(not fileName):
        return Prediction(**{"prediction": "", "message": "Invalid file"})
    
    # If the video file is not in 720x720, change it
    status = check_video_resolution(fileName)
    
    if(status == 1):
        convert_to_720x720(fileName)
    elif(status == 2):
        return Prediction(**{"prediction": "", "message": "Could not change resolation"})
    else:
        pass
    
    # Extract skeleton
    x, y = extract_skeleton(fileName)
    print(x.shape, y.shape)

    # Predict sign
    predicted_class = get_resource('lstm_model').predict(x, y)

    remove_video_file(fileName)

    if(not predicted_class):  
        return Prediction(**{"prediction": "", "message": "Could not predict sign"})

    
    return Prediction(**{"prediction": predicted_class, "message": "Success"})


@router.post("/text", response_model=Prediction)
def upload(landmarkObj: JsonLandmark):

    # Extract x and y
    x, y = get_resource('lstm_model').json_to_numpy(landmarkObj)

    if(not x and not y):
        return Prediction(**{"prediction": "", "message": "Invalid landmarks object"})

    # Predict sign
    predicted_class = get_resource('lstm_model').predict(x, y)

    if(not predicted_class):  
        return Prediction(**{"prediction": "", "message": "Could not predict sign"})

    
    return Prediction(**{"prediction": predicted_class, "message": "Success"})