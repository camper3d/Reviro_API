from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get('/tasks')
def get_tasks():
    return tasks_db

@app.post('/tasks', response_model=Task)
def create_task(task: Task):
    db_tasks.append(task)
    return task

@app.put('/tasks/{task_id}', response_model=Task)
def update_task(task_id: int, updated_task: Task):
    for i, task in enumerate(db_tasks):
        if task.id == task_id:
            db_tasks[i] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail='Задача не найдена')

@app.delete('/tasks/{task_id}')
def delete_task(task_id: int):
    for i, task in enumerate(db_tasks):
        if task.id == task_id:
            del db_tasks[i]
            return {'msg': 'Задача удалена'}
    raise HTTPException(status_code=404, detail= 'Задача не найдена')