import csv
import time

import requests
from fastapi import File, UploadFile, BackgroundTasks, APIRouter
from pydantic import BaseModel

router = APIRouter()


class FileProcessStatus(BaseModel):
    status: str
    result: str = None


file_process_statuses = {}


@router.post("/file")
async def process_file(file: UploadFile = File(default=None), background_tasks: BackgroundTasks = BackgroundTasks()):
    file_process_statuses[file.filename] = FileProcessStatus(status="processing")

    background_tasks.add_task(process_file_background, file)

    return {"message": "File received", "filename": file.filename}


def process_file_background(file):
    contents = file.file.read()

    results = []
    reader = csv.DictReader(contents.decode('utf-8').splitlines())
    for row in reader:
        user_id = row['userId']
        title = row['title']
        body = row['body']

        result = process_row(user_id, title, body)
        results.append(result)

        time.sleep(0.143)  # limit to 7 requests per second

    file_process_statuses[file.filename] = FileProcessStatus(status="complete", result=results)


def process_row(user_id, title, body):
    try:
        response = requests.post("https://jsonplaceholder.typicode.com/posts",
                                 json={"userId": user_id, "title": title, "body": body})
        post_id = response.json()['id']
        return {"userId": user_id, "result": "success", "postId": post_id}
    except:
        return {"userId": user_id, "result": "failed"}


@router.get("/file/{filename}/status")
async def get_file_status(filename):
    return file_process_statuses.get(filename)


@router.get("/file/{filename}/result")
async def get_file_result(filename):
    return file_process_statuses.get(filename).result
