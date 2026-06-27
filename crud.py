from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI()

todos=[]

class Todo(BaseModel):
    id:int
    tital:str
    isComplite:bool
    
@app.post("/todos")
def creat_todos(todo:Todo):
    todos.append(todo)
    return{
        "message": "Todo created successfully"
    }

@app.get("/todos")
def get_todoes():
    return todos

# specifc todo
@app.get("/todos/{todo_id}")
def get_todo(todo_id:int):
    for todo in todos:
        if todo.id==todo_id:
            return todo
    return{"error":"invailid todo id"}

# update todo
@app.put("/todos/{todo_id}")
def update_todo(todo_id:int,updatTodo:Todo):
    for index,todo in enumerate(todos):
        if todo.id==todo_id:
            todos[index]=updatTodo
            return{
                "massege":"update data",
                "data":updatTodo
            }
    return{"error":"invailid todo id"}


# delete todo
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id:int):
    for index,todo in enumerate(todos):
        if todo.id==todo_id:
            todos.pop(index)
            return{"messege":"todo delete successfull"}
    return{"error":"invailid todo"}
    
