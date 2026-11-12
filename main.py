from asyncio.windows_events import NULL

from fastapi import FastAPI, HTTPException

app = FastAPI()

# "מסד נתונים" בזיכרון
tasks = []
counter = 1

@app.get("/tasks")
def get_tasks(priority: int=None):
    for task in tasks:
        if task["priority"]==None:
            task["priority"] = 2
    filter_tasks = []
    if priority:
        if priority < 1 or priority > 3:
            raise HTTPException(status_code=400, detail="Priority must be between 1 and 3")
        for task in tasks:
            if task["priority"] == priority:
                filter_tasks.append(task)
        return filter_tasks
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["priority"] == None:
            task["priority"] = 2
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks")
def add_task(task: dict):
    global counter
    priority = 2
    if task.get("priority"):
        priority = task.get("priority")
    if priority<1 or priority>3:
        raise HTTPException(status_code=400, detail="Priority must be between 1 and 3")
    new_task = {
        "id": counter,
        "title": task.get("title"),
        "owner": task.get("owner"),
        "priority": priority
    }
    tasks.append(new_task)
    counter += 1
    return new_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")
