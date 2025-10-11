import os
from notion_client import Client
from dotenv import load_dotenv
load_dotenv()


NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID  = os.getenv("NOTION_DATABASE_ID")

notion = Client(auth=NOTION_TOKEN)

def fetch_notion_tasks():
    """
    Fetch tasks from the configured Notion database.
    Returns list[dict] with text, source, tags.
    """
    pages = notion.databases.query(database_id=DATABASE_ID)["results"]
    tasks = []
    for page in pages:
        props = page["properties"]
        title = props.get("Name", {}).get("title", [])
        text  = title[0]["plain_text"] if title else "Untitled"
        tags  = [t["name"] for t in props.get("Tags", {}).get("multi_select", [])]
        tasks.append({
            "text": text,
            "source": "notion",
            "tags": tags
        })
    return tasks
