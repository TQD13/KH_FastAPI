from typing import Annotated
from fastapi import BackgroundTasks, FastAPI, Depends

app = FastAPI()


def write_notification(email: str, message=""):  # Create a task function
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


@app.post("/send-notification_1/{email}")
async def send_notification_1(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(
        write_notification, email, message="Some notification"
    )  # Add the background task
    return {"message": "Notification sent in the background"}


# --------------------------------------------------------------------------------------------------------------
# Dependency Injection


def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message)


def get_query(background_tasks: BackgroundTasks, q: str | None = None):
    if q:
        message = f"found query: {q}\n"
        background_tasks.add_task(write_log, message)
    return q


@app.post("/send-notification/{email}")
async def send_notification(
    email: str, background_tasks: BackgroundTasks, q: Annotated[str, Depends(get_query)]
):
    message = f"message to {email}\n"
    background_tasks.add_task(write_log, message)
    return {"message": "Message sent"}
