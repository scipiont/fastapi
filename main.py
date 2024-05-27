from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI()

# Модель данных для задачи
class Task(BaseModel):
    title: str = Field(..., example="Название задачи")
    description: Optional[str] = Field(None, example="Описание задачи")
    completed: bool = Field(False, example=False)

# Модель данных для обновления задачи
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, example="Название задачи")
    description: Optional[str] = Field(None, example="Описание задачи")
    completed: Optional[bool] = Field(None, example=False)

# Временное хранилище для задач
tasks = []
task_id_counter = 1

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks

@app.get("/tasks/{id}", response_model=Task)
def get_task(id: int):
    for task in tasks:
        if task["id"] == id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    global task_id_counter
    task_dict = task.dict()
    task_dict["id"] = task_id_counter
    tasks.append(task_dict)
    task_id_counter += 1
    return task_dict

@app.put("/tasks/{id}", response_model=Task)
def update_task(id: int, task_update: TaskUpdate):
    for task in tasks:
        if task["id"] == id:
            if task_update.title is not None:
                task["title"] = task_update.title
            if task_update.description is not None:
                task["description"] = task_update.description
            if task_update.completed is not None:
                task["completed"] = task_update.completed
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{id}", response_model=Task)
def delete_task(id: int):
    for task in tasks:
        if task["id"] == id:
            tasks.remove(task)
            return task
    raise HTTPException(status_code=404, detail="Task not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)