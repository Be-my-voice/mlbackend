import os
import glob

from app.dto.sign_list_res_dto import SignRecordList, SignRecord

def list_signs():
    dataset_path = os.getenv("DATASET_PATH")
    sign_list = SignRecordList(records=[])

    try:
    # Iterate through subdirectories in the dataset folder
        for dir_name in os.listdir(dataset_path):
            dir_path = os.path.join(dataset_path, dir_name)

            if os.path.isdir(dir_path):
                # Count files with the naming pattern "<dir_name>_<number>.csv"
                matching_files = glob.glob(os.path.join(dir_path, f"{dir_name}_*.csv"))
                count = len(matching_files)

                # Create a SignRecord object and add it to the list
                sign_record = SignRecord(name=dir_name, number_of_records=count)
                sign_list.addRecord(sign_record)

    except Exception as e:
        print(f"Error: {e}")
        sign_list.setMessage("Fetching failed")
        return sign_list

    sign_list.setMessage("Successful")
    return sign_list

