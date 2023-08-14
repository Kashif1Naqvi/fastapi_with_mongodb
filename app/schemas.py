from datetime import datetime
from pydantic import BaseModel, EmailStr, constr, Field
from typing import Optional
from bson.objectid import ObjectId

class UserBaseSchema(BaseModel):
    name: str
    email: str
    address: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
    
    
    class Config:
        orm_mode = True

class AssignRole(BaseModel):
    
    email: str
    role: str
    
    class Congig:
        orm_mode = True


class CreateUserSchema(UserBaseSchema):
    password : constr(min_length=8)
    passwordConfirm: str
    verified: bool = False
    
    
class LoginUserSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)
    



class UserResponseSchema(UserBaseSchema):
    id: str
    pass


class UserResponse(BaseModel):
    status: str
    user: UserResponseSchema
    
    
class TokenData(BaseModel):
    id: Optional[str] = None
    

class PostBaseModel(BaseModel):
    title: str
    content: str
    published: bool = True
    
    
class PostCreate(PostBaseModel):
    user: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}





class CreateRole(BaseModel):
    user_id: str
    role_name: str
    
    
    

class Permissions(BaseModel):
    role_id: str
    can_create: bool = False
    can_edit: bool = False
    can_add: bool = False
    can_update: bool = False
    can_delete: bool = False
    can_view: bool = False

# New tables technique

class UserRole(BaseModel):
    role_name: str
    role_description: str
    
    class Config:
        orm_mode = True
        

class UsersRole(BaseModel):
    user_id: str
    role_id: str
    
    class Config:
        orm_mode = True
    
class Screen(BaseModel):
    name: str
    description: str
    
    class Config:
        orm_mode = True

class ScreensRoles(BaseModel):
    role_id: str
    screen_id: str
    
    class Config:
        orm_mode = True

class ScreenPermission(BaseModel):
    screen_id: str
    
    class Config:
        orm_mode = True

class CreateScreenLink(BaseModel):
    screen_id: str
    link_text: str
    link_description: str
    
    
    class Config:
        orm_mode = True

class LinkContent(BaseModel):
    
    screen_id: str
    link_id: str
    
    class Config:
        orm_mode = True

class LinksDisplay(BaseModel):
    screen_id: str
    
    class Config:
        orm_mode = True


class LinkDisplay(BaseModel):
    screen_id: str
    link_id: str
    
    class Config:
        orm_mode = True

class LinksUsers(BaseModel):

    user_id: str
    screen_id: str
    link_id: str


    class Config:
        orm_mode = True
    
class RolesLinks(BaseModel):
    role_id: str
    link_id: str
    
    
    class Config:
        orm_mode = True



class ScreenRoles(BaseModel):
    role_id: str
    screen_id: str
    
    
    class Config:
        orm_mode = True

class ScreenLinks(BaseModel):
    role_id: str
    screen_id: str
    link_id: str
    
    
    class Config:
        orm_mode = True

class CreateEmployee(BaseModel):
    
    first_name: str
    last_name: str
    email: str
    nick_name: str  = None
    department_name: str  = None
    location_name: str  = None
    designation: str  = None
    employment_type: str  = None
    employee_status: str  = None
    date_of_joining: str  = None
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    
    class Config:
        orm_mode = True
        

class Search(BaseModel):
    search: str= None        

class ViewEditEmployee(BaseModel):
    id: str
    
    class Config:
        orm_mode = True
        
        
class EditEmployee(CreateEmployee):
    id: str
    
    class Config:
        orm_mode = True


class EmployeeOut(BaseModel):
    
    id: str = Field(default_factory=str, alias="_id")
    first_name: str
    last_name: str
    email: str
    nick_name: str  = None
    department_name: str  = None
    location_name: str  = None
    designation: str  = None
    employment_type: str  = None
    employee_status: str  = None
    date_of_joining: str  = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        




class Test(BaseModel):
    
    id: str = Field(default_factory=str, alias="_id")
    name: str
    surname: str
    

    class Config:
        
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        
