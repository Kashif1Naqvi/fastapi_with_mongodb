from fastapi import Depends, HTTPException
from typing import List
from bson.objectid import ObjectId
import logging as logger
from app.database import User, Role, UserRole, UserPermission
from ..import oauth2, utils



class RoleChecker:
    def __init__(self, allowed_roles: List):
        self.allowed_roles = allowed_roles #utils.get_roles(Role)

    def __call__(self, user: User = Depends(oauth2.require_user)):
        print("user=======>", user)
        if user['role'] not in self.allowed_roles:
            logger.debug(f"User with role {user['role']} not in {self.allowed_roles}")
            raise HTTPException(status_code=403, detail="You have not a permission to performe action.")
        
        

class RolePermissionChecker:
    def __init__(self):
        self.roles = utils.get_roles(UserRole)
        self.permission = utils.get_roles(UserPermission)
        
    def __call__(self, user: User = Depends(oauth2.require_user)):
        
        print("====================================================LOGIN_USER=================================================")
        print(user)
        print("====================================================END LOGIN_USER================================================= /n /n /n /n \n \n")
        
        
        print("====================================================ROLES=================================================")
        print(self.roles)
        print("====================================================END ROLES================================================= /n /n /n /n \n \n")
        
        print("====================================================PERMISSIONS=================================================")
        print(self.permission)
        print("====================================================END PERMISSIONS================================================= /n /n /n /n \n \n")
        
        for role in self.roles:
            if(role["_id"] == ObjectId(str(user['id']))):
                if(role['role_name'] == user['role']):
                    pass            
        else:
            logger.debug(f"User with role {user['role']} not in {self.roles}")
            raise HTTPException(status_code=403, detail="You have not a permission to performe action.")
        
        
