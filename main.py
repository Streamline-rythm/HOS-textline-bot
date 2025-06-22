import os
import json
import uvicorn
import asyncio
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query

load_dotenv()

access_token = os.getenv('access_token')
base_url = os.getenv('base_url')

if not access_token or not base_url:
    raise ValueError("access token is not loaded")

app = FastAPI(
    title = "Textline Replies Retriever",
    description = "API to retrieve replied messages from textline",
    version = "1.0.0",
)

@app.get("/get_replied_img")
async def get_replied_img(
    after_uuid: str = Query(..., description="The uuid of parent message"),
    group_uuid: str = Query(..., description="The uuid of group"),
    page: int = Query(..., description="first page of conversation"),
    page_size: int = Query(..., description="number of returned latest replied message"),
    phone_number: str = Query(..., description="The phone number of client"),
):
    url = f"{base_url}?after_uuid={after_uuid}&group_uuid={group_uuid}&page={page}&page_size={page_size}&phone_number={phone_number}&access_token={access_token}"
    print(f"get_request_url = {url}")

    for i in range(30):
        print(f"{i}th loop")
        respond = requests.get(url)
        data = respond.json() 
        posts = data.get("posts")

        for post in posts:
            if post["attachments"]:
                return post
        
        await asyncio.sleep(10)
    
    return {
        "body": "not image"
        }

@app.get("/get_replied_message")
async def get_replied_message(
    after_uuid: str = Query(..., description="The uuid of parent message"),
    group_uuid: str = Query(..., description="The uuid of group"),
    page: int = Query(..., description="first page of conversation"),
    page_size: int = Query(..., description="number of returned latest replied message"),
    phone_number: str = Query(..., description="The phone number of client"),
):
    url = f"{base_url}?after_uuid={after_uuid}&group_uuid={group_uuid}&page={page}&page_size={page_size}&phone_number={phone_number}&access_token={access_token}"
    print(f"get_request_url = {url}")

    for i in range(30):
        print(f"{i}th loop")
        respond = requests.get(url)
        data = respond.json() 
        posts = data.get("posts")

        if posts:
            post = posts[0]
            if not post["attachments"]:
                return post
            if post["attachments"]:
                return {
                    "body": "not message"
                }
        await asyncio.sleep(10)
    
    return {
        "body": "not message"
        }

@app.get("/test")
async def test():
    return {"result": "success"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, proxy_headers=True)
