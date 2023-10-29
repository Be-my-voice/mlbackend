from fastapi import APIRouter
from app.dto.base64video_dto import Base64Video

from app.utils.utils import base64ToVideo, remove_video_file
from app.services.skeleton_extraction import extract_skeleton
from app.services.video_adjustment import check_video_resolution, convert_to_720x720
from app.utils.async_utils import get_resource


router = APIRouter(
    tags=["predict"],
    responses={404: {"description": "Not found"}},
)

@router.post("/video")
def upload(video: Base64Video):
    # Convert base64 to mp4
    fileName = base64ToVideo(video.data)

    if(not fileName):
        return {"message": "Invalid file"}
    
    # If the video file is not in 720x720, change it
    status = check_video_resolution(fileName)
    
    if(status == 1):
        convert_to_720x720(fileName)
    elif(status == 2):
        return {"message": "Could not change resulation"}
    else:
        pass
    
    # Extract skeleton
    x, y = extract_skeleton(fileName)
    print(x.shape, y.shape)

    # Predict sign
    predicted_class = get_resource('lstm_model').predict(x, y)

    remove_video_file(fileName)

    if(not predicted_class):
        return {"message:" "Could not predict sign"}

    
    return {"sign": predicted_class}
