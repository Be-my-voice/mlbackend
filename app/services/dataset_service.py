import os
import glob
import csv
import json

from app.dto.sign_list_res_dto import SignRecordList, SignRecord
from app.dto.record_list_res_dto import RecordList
from app.dto.record_landmarks_dto import JsonLandmarkRes

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


# List ids of all csv files in particular sign name
def list_records(class_name: str):
    dataset_path = os.getenv("DATASET_PATH")
    subdirectory_path = os.path.join(dataset_path, class_name)

    record_list = RecordList(records=[], message="")
    
    # Check if the directory exists
    if not os.path.exists(subdirectory_path):
        record_list.setMessage("Successful")
        return record_list
    
    # List files in the directory
    files = os.listdir(subdirectory_path)
    
    # Iterate through the files and extract IDs from filenames
    for file_name in files:
        if file_name.endswith('.csv'):
            # Split the filename by '_' and check if it has the required format
            parts = file_name.split('_')
            if len(parts) == 2 and parts[1].endswith('.csv'):
                csv_id = parts[1][:-4]  # Remove the '.csv' extension
                record_list.addRecord(int(csv_id))
    
    record_list.setMessage("Successful")
    return record_list

# Function to read csv content and convert into json
def read_record(class_name: str, id: int):
    dataset_path = os.getenv("DATASET_PATH")
    subdirectory_path = os.path.join(dataset_path, class_name)
    file_name = class_name + '_' + id + '.csv'
    file_path = os.path.join(subdirectory_path, file_name)

    response = JsonLandmarkRes(landmarks=[], message="")

    if not os.path.exists(file_path):
        response.setMessage("Record does not exist")
        return response

    # Read CSV file and convert it to a list of lists
    data = []
    try:
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                data.append(row)
    except Exception as e:
        print(f"Error: {e}")
        response.setMessage("File read failed")
        return response

    # Read the CSV file and convert it to a JSON format

    try:
        json_data = []
        for row in data:
            json_data.append(row)
    except Exception as e:
        print(f"Error: {e}")
        response.setMessage("JSON conversion failed")

    response.setLandmarks(json_data)
    response.setLandmarks("Success")
    return response

