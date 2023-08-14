import pydantic
from fastapi import  status, HTTPException, Depends, APIRouter
from datetime import datetime
from bson.objectid import ObjectId
from .. import schemas, oauth2
from app.serializers import userSerializers
from ..database import Post
from .roleChecker import RoleChecker, RolePermissionChecker
pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str

router = APIRouter()

# view_resource = RoleChecker(['user', 'admin', 'learner'])
view_resource = RolePermissionChecker()
@router.get('/', dependencies=[Depends(view_resource)])
async def posts(user_id: str = Depends(oauth2.require_user)):

    list = []
    for i in Post.find():
        list.append(i)

    return {'status': 'success', "response":  list}

view_resource = RoleChecker(['user', 'admin', 'learner'])
@router.get('/{id}', dependencies=[Depends(view_resource)])
async def get_post(id: str, current_user: int = Depends(oauth2.require_user)):
    
    count = Post.count_documents({"_id": ObjectId(str(id))})
    
    
    if not ObjectId.is_valid(str(id)):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Post of id {id} is not valid")
    
    
    if count == 0:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Post of id {id} does not exist")
    
    post = userSerializers.postEntity(Post.find_one(ObjectId(str(id))))

    return post


create_resource = RoleChecker(['admin', 'user'])
@router.post('/', status_code=status.HTTP_201_CREATED, dependencies=[Depends(create_resource)])
def create_posts(post: schemas.PostCreate, current_user: int = Depends(oauth2.require_user)):
    post.user = ObjectId(current_user['id'])
    post.created_at = datetime.utcnow()
    post.updated_at = post.created_at
    Post.insert_one(post.dict())
    return {
        "message": "Post created successfully"
    }
    
delete_resource = RoleChecker(['admin', 'user'])
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(delete_resource)])
def delete_post(id: str, current_user: int = Depends(oauth2.require_user)):

    if not ObjectId.is_valid(id):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Post of id {id} does not exist")
    

    count = Post.count_documents({"_id": ObjectId(str(id))})
    if count == 0:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Post of id {id} does not exist")
    
    get_post = userSerializers.postEntity(Post.find_one(ObjectId(str(id))))
    
    
    if get_post['user'] != current_user["id"]:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail=f"Not Authorized for performing this action")
    
    
    post = Post.delete_one({"_id": ObjectId(str(id))})

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No post with this id: {id} found')
    
    return {
        "status_code": status.HTTP_204_NO_CONTENT, 
        "message": "post deleted succesfully",
    }

view_resource = RoleChecker(['user', 'admin'])
@router.put("/{id}")
def update_post(id: str, updated_post: schemas.PostBaseModel, current_user: int = Depends(oauth2.require_user)):
    
    count = Post.count_documents({"_id": ObjectId(str(id))})
    
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Post of id {id} does not exist")
    
    if count == 0:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Post of id {id} does not exist")
    
    get_post = userSerializers.postEntity(Post.find_one(ObjectId(str(id))))
    
    if(current_user['role'] != 'admin'):
        if get_post['user'] != current_user["id"]:
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail=f"Not Authorized for performing this action")
    
    dict = updated_post.dict(exclude_none=True)
    
    updated_post = Post.update_one(
        {'_id': ObjectId(id)}, {'$set': dict})

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_200_OK,
                        detail=f'No post with this id: {id} found')

    return  {
        "status_code": status.HTTP_200_OK, 
        "message": "post updated succesfully",
    }


  