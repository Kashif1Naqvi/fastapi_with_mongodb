from fastapi import APIRouter, Depends, HTTPException, status
from bson.objectid import ObjectId
from app.serializers.userSerializers import userResponseEntity
from .roleChecker import RoleChecker

from app.database import User, Role, UserRole, UserPermission
from ..import schemas, oauth2, utils


router = APIRouter()

allow_create_resource = RoleChecker(["admin"])
@router.post('/assign_roles', dependencies=[Depends(allow_create_resource)])
def assign_roles(assign_role: schemas.AssignRole ,user_id: str = Depends(oauth2.require_user)):
    
    roles = utils.get_roles(Role)
    
    
    email = assign_role.dict()['email']
    desired_role = assign_role.dict()['role']
    
    count = User.count_documents({"email": str(email)})
    
    role_count = Role.count_documents({"role": str(desired_role)})
    
    if count == 0:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"User for email {email} does not exist")
    
    if role_count == 0:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"please used only given roles => {','.join(role if role != 'admin' else '' for role in roles)} ")
    
    res = userResponseEntity(User.find_one({"email": str(email)}))
    
    user_id = user_id["id"]
    
    user = userResponseEntity(User.find_one(ObjectId(str(user_id))))
    
    if user['role'] != res['role']:
        dict = assign_role.dict(exclude_none=True)
        User.update_one(
            {'_id': ObjectId(str(res['id']))}, {'$set': dict})

        return {
            "message": f"user email {email} role {res['role']} updated to {desired_role}",
            "loged_in_user": user
        }
    
    return {
        "user": user
    }

@router.post('/create_role')
def create_role(roles: schemas.CreateRole):
    role = roles.dict()
    
    if not ObjectId.is_valid(str(role['user_id'])):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Post of id {role['user_id']} is not valid")
    
    user_count = User.count_documents({"_id": ObjectId(str(role['user_id']))})
    
    if user_count == 0:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"User for id {role['user_id']} does not exist")
    
    role_count = UserRole.count_documents(role)
    
    if role_count > 0:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Role already exist")
    
    
    UserRole.insert_one(role)
    
    return {
        "message": "role create successfully...",
        "roles": role,
        "user_count": user_count
    }


@router.post("/create_permission")
def create_permission(permission: schemas.Permissions):
    permission = permission.dict()
    
    if not ObjectId.is_valid(str(permission['role_id'])):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Permission of role_id {permission['role_id']} is not valid")
    
    role_count = UserRole.count_documents({"_id": ObjectId(str(permission['role_id']))})
    
    if role_count == 0:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Role for id {permission['role_id']} does not exist")
    
    permision_count = UserPermission.count_documents(permission)
    if permision_count > 0:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Permission already exist")
    
    UserPermission.insert_one(permission)
    
    
    
    
    return {
        "message": "permission create successfully...",
        "permissions": permission
    }

