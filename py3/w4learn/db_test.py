from fastapi import FastAPI,Query,HTTPException
from pydantic import BaseModel,Field



app = FastAPI()
class Person(BaseModel):
    name:str=Field(min_length=1,max_length=10)
user_db=[]

@app.post("/users")
def create_users(users:Person):
    new_user={
        "name":users.name,
        "id":len(user_db)+1
    }
    user_db.append(new_user)
    return {
        "message":f"User{new_user["name"]} created successfully"
    }

@app.get("/users")
def get_users(limit:int=Query(default=5,ge=1,le=10)):
    return user_db[:limit]

@app.get("/users/{user_id}")
def get_user(user_id:int):
    for it in user_db:
        if it["id"] == user_id:
            return it
    raise HTTPException(status_code=404,detail="User not found")

@app.put("/users/{user_id}")
def update_user(user_id:int,user: Person):
    for it in user_db:
        if it["id"] == user_id:
            it["name"] = user.name
            return {
                "message":f"User updated successfully",
                "data":it
            }
    raise HTTPException(status_code=404,detail="User not found")

@app.delete("/users/{user_id}")
def delete_user(user_id:int):
    for it in user_db:
        if it["id"] == user_id:
            user_db.remove(it)
            return {
                "message":f"User{it.name} deleted successfully"
            }
    raise HTTPException(status_code=404,detail="User not found")

# @app.put("/users/{user_id}")
# def update_user(user_id:int,user: Person):




