import csv
import time

import requests
from fastapi import File, UploadFile, BackgroundTasks, APIRouter

from service.models import FileModel, FileProcessStatus, Result

router = APIRouter()

file_process_statuses = {}


@router.post("/file")
async def process_file(file: UploadFile = File(default=None), background_tasks: BackgroundTasks = BackgroundTasks()) \
        -> dict:
    file_process_statuses[file.filename] = FileProcessStatus(status="processing")

    background_tasks.add_task(process_file_background, file)

    return {"message": "File received", "filename": file.filename}


def process_file_background(file):
    contents = file.file.read()

    results = []
    reader = csv.DictReader(contents.decode('utf-8').splitlines())
    for row in reader:
        file_model = FileModel(**row)

        result = process_row(file_model.userId,
                             file_model.title,
                             file_model.body)
        results.append(result)

        time.sleep(1)  # limit to 7 requests per second

    file_process_statuses[file.filename] = FileProcessStatus(status="complete", result=results)


def process_row(user_id: int, title: str, body: str) -> dict:
    try:
        response = requests.post("https://jsonplaceholder.typicode.com/posts",
                                 json={"userId": user_id, "title": title, "body": body})
        post_id = response.json()['id']
        return {"userId": user_id, "result": "success", "postId": post_id}
    except:
        return {"userId": user_id, "result": "failed"}


@router.get("/file/{filename}/status")
async def get_file_status(filename: str) -> str:
    if file_process_statuses.get(filename):
        return file_process_statuses.get(filename).status
    else:
        return "File doesn't exists"


@router.get("/file/{filename}/result")
async def get_file_result(filename: str) -> list[Result] | str:
    if file_process_statuses.get(filename):
        result = file_process_statuses.get(filename)
        return result.result
    else:
        return "File doesn't exists"
