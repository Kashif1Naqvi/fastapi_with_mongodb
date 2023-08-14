from passlib.context import CryptContext
from fastapi import  status, HTTPException
from .database import UsersRoles, UserScreenRole, Screen

from bson.objectid import ObjectId

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def hash_password(password):
    return pwd_context.hash(password)
    


def verify_password(password: str, hash_password: str):
    return pwd_context.verify(password , hash_password)


def get_roles(Role_collection):
    return [i for i in Role_collection.find()]
    
        
    

def check_valid(input_string):
    import re
    pattern = re.compile(r"^(\w+)(,\s*\w+)*$")
    
    if pattern.match(input_string) == None:
        return False
    else:
        return True

def is_valid_id(ids):
    
    for id in ids:
        if not ObjectId.is_valid(str(id)):
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"id {id} is not valid")
        
        continue        

def is_dublicate(ids):
        d={}
        for id in ids:
            if id not in d:
                d[id] = 1
            else:
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"id {id} is already available in string please don't use dublicate id")
        return False    
    
    
def is_exists(model, ids):
    
    for id in ids:
        count = model.count_documents({"_id": ObjectId(str(id))})
        
        if count == 0:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"id {id} is does not exist")
       
        continue
      
def insert_role(role_id, ids, model):
        
    for id in ids:
        count_roles_users_exist = model.count_documents({"user_id": ObjectId(str(id))})
        
        if(count_roles_users_exist > 0):
            user_obj = {"user_id": ObjectId(str(id)), "role_id": ObjectId(str(role_id))}
            data = model.find_one({"user_id": ObjectId(str(id))})
            model.update_one({"_id": ObjectId(str(data["_id"]))}, {'$set': user_obj})
        else:
            model.insert_one({"user_id": ObjectId(str(id)), "role_id": ObjectId(str(role_id))})
            

# def assign_role_to_users(users_roles_model, User, Role):
#     data = UsersRoles.find_one({"user_id": ObjectId(str(user_id))})

#     for i in users_roles_model.find():    
    
#         role_id = i['role_id']
#         user_id = i['user_id']
        
#         user = User.find_one({"_id": ObjectId(str(user_id))})
#         role = Role.find_one({"_id": ObjectId(str(role_id))})
#         print("role", role)
#         print("user", user)
#         users_roles_model.insert_one({"user_id": ObjectId(str(user['_id'])), "role_id": ObjectId(str(role["_id"]))})
#         # user_obj = {"role": role['role_name'], "exclude_none":True}
                    
#         # User.update_one({"_id": ObjectId(str(user['_id']))}, {'$set': user_obj})

        
        

def validate_id(value, model, id):

    if not ObjectId.is_valid(str(value)):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f" {id} is not valid")
    
    if(len(str(value).replace(" ", "").split(',')) > 1):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"You cannot add multiple  id's")
    if(model is not None):
        count_role = model.count_documents({"_id": ObjectId(str(value))})
        
        if count_role == 0:
            
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"{id} {value} does not exist.")


def record_exists(model, key, value, label, screen_id):
    
    if(model is None or key is None or value is None or label is None):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Please pass all parameters model_name, key, value, label in sequence")
    if(screen_id):
        count_role = model.count_documents({key: value, "screen_id": screen_id})
    else:
        count_role = model.count_documents({key: value})
    
    if count_role > 0:
        
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"{label} {value} already exist. please try another")

def is_none(label, is_error, value):
    if(is_error):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"{label} {value} already exist. please try another")
    
    

def get_screen_id(user_id):
    data = UsersRoles.find_one({"user_id": ObjectId(str(user_id))})
    screens =  list(UserScreenRole.aggregate([{"$match": {"role_id": ObjectId(str(data['role_id']))}}]))

    screen_list = []
    screen_ids = []
    for screen in screens:
        if('screen_id' in screen):
            if(screen['screen_id'] not in screen_ids):
                screen_ids.append(screen['screen_id'])
    if(screen_ids):            
        for screen_id in screen_ids:
            screen_list += list(Screen.aggregate([{"$match": {"_id": ObjectId(str(screen_id))}}]))
 
    
    return screen_list