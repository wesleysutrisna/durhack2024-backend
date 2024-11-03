from enum import Enum
from image_check import detect_object_in_image

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import shutil
import os

app = FastAPI()
today = '02-11-2024'

# Directory to save uploaded images
UPLOAD_DIRECTORY = "./uploads"

# Ensure upload directory exists
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


class QuestItem(BaseModel):
    item: str
    id: int
    date: str


class User(BaseModel):
    id: int
    username: str
    items_found_today: int
    total_items_found: int
    score: int


dictQuestItems = {
    0: QuestItem(id=0, item='stairs', date='02-11-2024'),
    1: QuestItem(id=1, item='bridge', date='02-11-2024'),
    2: QuestItem(id=2, item='lake', date='02-11-2024'),
    3: QuestItem(id=3, item='tree', date='03-11-2024'),
    4: QuestItem(id=4, item='bike', date='03-11-2024')
}

dictUsers = {
    0: User(id=0, username='Jack', items_found_today=0, total_items_found=0, score=0),
    1: User(id=1, username='Mark', items_found_today=0, total_items_found=0, score=0),
    2: User(id=2, username='Wes', items_found_today=0, total_items_found=0, score=0),
    3: User(id=3, username='Eky', items_found_today=0, total_items_found=0, score=0),
    4: User(id=4, username='Mos', items_found_today=0, total_items_found=0, score=0)
}


# return only words with today's day
@app.get('/quest-items')
def index() -> dict[str, dict[int,QuestItem]]:
    quest_items_today = {
        idx: quest_item for idx, quest_item in enumerate(
            quest_item for quest_item in dictQuestItems.values() if quest_item.date == today
        )
    }
    return {'targetWords': quest_items_today}


# Endpoint for uploading images
@app.post('/upload-image/{user_id}/{quest_item_id}')
async def upload_image(user_id: int, quest_item_id: int, file: UploadFile = File(...)):
    # Check if the user exists
    if user_id not in dictUsers:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if quest item is valid
    if quest_item_id in dictQuestItems and dictQuestItems[quest_item_id].date == today:
        quest_item = dictQuestItems[quest_item_id].item
    else:
        raise HTTPException(status_code=404, detail="Invalid quest_item_ID")

    # Save the uploaded file
    file_location = os.path.join(UPLOAD_DIRECTORY, f"user_{user_id}_{file.filename}")

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Here, you should implement your image processing logic
    # For now, we will assume it always finds the word (you'll want to replace this with real logic)
    item_found = detect_object_in_image(file_location, quest_item)  # Placeholder for your actual image processing result
    if item_found:
        dictUsers[user_id].items_found_today += 1
        dictUsers[user_id].total_items_found += 1
        if dictUsers[user_id].items_found_today == 1:
            dictUsers[user_id].score += 50
        elif dictUsers[user_id].items_found_today == 1:
            dictUsers[user_id].score += 100
        elif dictUsers[user_id].items_found_today == 3:
            dictUsers[user_id].score += 150

    try:
        os.remove(file_location)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not delete file: {e}")


    return {
        "image_file_name": file_location,
        "user_id": user_id,
        "quest_item": quest_item,
        "item_found": item_found
    }

