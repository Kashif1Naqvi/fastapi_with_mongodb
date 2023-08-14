import pydantic
from fastapi import  Form, File, UploadFile, status, HTTPException, Depends, APIRouter, Query

from bson.objectid import ObjectId
from .. import schemas, oauth2, utils
from app.serializers import userSerializers
from ..database import User, Role, Screen, Link, UserScreenRole, UsersRoles, Employee
from fastapi_pagination import Page, paginate
from typing import TypeVar, Generic

from fastapi_pagination.default import Page as BasePage, Params as BaseParams

T = TypeVar("T")


class Params(BaseParams):
    size: int = Query(5, ge=1, le=1_000, description="Page size")


class Page(BasePage[T], Generic[T]):
    __params_type__ = Params


pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str

router = APIRouter()



#All the roles that is related to users will show here
@router.get('/roles_list')
def roles():
    list = []
    for i in Role.find():
        list.append(i)

    return {'status': 'success', "roles":  list}
    
# All users belong to application will show
@router.get('/users_list')
def users_list():
    list = []
    for i in User.find():
        list.append(i)

    return {'status': 'success', "users":  list}


# All screens belong to application will show
@router.get("/list_screen")
def screens_list():
    list = []
    for i in Screen.find():
        list.append(i)

    return {'status': 'success', "screens":  list}

# All links belong to application will show
@router.get('/links_list')
def links_lists():
    list = []
    for i in Link.find():
        list.append(i)

    return {'status': 'success', 'message': "links lists with every screen id" , "list":  list}

# All role assign screens list
@router.get('/assign_screen_role')
def assign_screen_role_list():
    list = []
    for i in UserScreenRole.find():
        list.append(i)

    return {'status': 'success', 'message': "All role assign screens list" , "list":  list}

# Create role for user
@router.post('/create_role')
def create_role(role: schemas.UserRole):
    role_dict = role.dict()    
    
    utils.record_exists(Role, 'role_name', role_dict['role_name'], 'Role', None)
    
    Role.insert_one(role_dict)
    
    return {
        "Message": "Role created successfully..."
    }


# create screen e.g Dashboard for users to see when login
@router.post("/create_screen")
def create_screen(screen: schemas.Screen):
    screen_obj = screen.dict()
    value = screen_obj['name']
    utils.record_exists(Screen, 'name', value, 'Screen', None)
    Screen.insert_one(screen_obj)
    return {
        "Message": "Screen created successfully.",
    }

# create links for specific screen e.g Dashboard have links home, service, contact etc 
@router.post("/create_screen_links")
def create_link(links: schemas.CreateScreenLink):
    link = links.dict()
    screen_id = link['screen_id']
    utils.validate_id(screen_id, Screen, 'screen_id')
    
    screen = userSerializers.userScreen(Screen.find_one({"_id" : ObjectId(str(screen_id))}))
    
    if(screen is None):
        
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"screen_id  {screen_id} does not exist.")    

    utils.record_exists(Link, 'link_text', str(link['link_text']), 'Link', screen_id=screen_id)
    
    Link.insert_one(link)
    return {
        "message": "screen link created successfully",
        "links": link
    }

# assign created role to user
@router.post('/assign_user_role')
def assign_user_role(users_roles: schemas.UsersRole):

    roles_dict = users_roles.dict()
    
    
    if(not utils.check_valid(roles_dict['user_id'])):
        return {
            "Message": "Comma seprated users required"
        }
    
    utils.validate_id(roles_dict["role_id"], None, "role_id")
    user_ids = roles_dict['user_id'].replace(' ', '').split(',')
    utils.is_valid_id(user_ids)
    utils.is_dublicate(user_ids)
    utils.is_exists(User, user_ids)
    
    role = userSerializers.userRole(Role.find_one({"_id" :ObjectId(str(roles_dict['role_id']))}))
    
    utils.insert_role(role["role_id"], user_ids, UsersRoles)
    
    # utils.assign_role_to_users(UsersRoles, User, Role)

    return {
        "Message": "Roles assign successfully."
    }
    

# Assign links for specifc screen for populating at specific screen
@router.post("/assign_screen_role")
def assign_screen_role(link_content: schemas.ScreenRoles):
    content = link_content.dict()
    screen_id = content['screen_id']
    role_id = content['role_id']
    utils.validate_id(screen_id, Screen, 'screen_id')
    utils.validate_id(role_id, Role, 'role_id')
    
    role = userSerializers.userRole(Role.find_one({"_id" : ObjectId(str(role_id))}))
    screen = userSerializers.userScreen(Screen.find_one({"_id" : ObjectId(str(screen_id))}))
    utils.is_none('role', role is None, role_id)
    utils.is_none('screen_id', screen is None, screen_id)
    
    count_role = UserScreenRole.count_documents({"screen_id": ObjectId(str(screen['screen_id'])), "role_id": ObjectId(str(role['role_id']))})
    if count_role > 0:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"screen_id ,role_id {screen_id} {role_id} already exist.")
    
    UserScreenRole.insert_one({"screen_id": ObjectId(str(screen['screen_id'])), "role_id": ObjectId(str(role['role_id']))})
    
    return {
        "message": "role to screen assigned successfully",
        "links": content
    }


# Assign links for specifc screen for populating at specific screen
@router.post("/assign_screen_link")
def assign_screen_link(link_content: schemas.ScreenLinks):
    content = link_content.dict()
    screen_id = content['screen_id']
    role_id = content['role_id']
    link_id = content['link_id']
    utils.validate_id(screen_id, Screen, 'screen_id')
    utils.validate_id(role_id, Role, 'role_id')
    utils.validate_id(link_id, Link, 'link_id')
    
    role = userSerializers.userRole(Role.find_one({"_id" : ObjectId(str(role_id))}))
    screen = userSerializers.userScreen(Screen.find_one({"_id" : ObjectId(str(screen_id))}))
    link = userSerializers.link_display(Link.find_one({"_id" : ObjectId(str(link_id))}))
    
    utils.is_none('role', role is None, role_id)
    utils.is_none('screen_id', screen is None, screen_id)
    utils.is_none('link_id', link is None, link_id)
    
    count_link = Link.count_documents({"_id" : ObjectId(str(link_id)), "screen_id": screen['screen_id']})
    
    if(count_link == 0):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"screen_id , link_id  {screen_id} {link_id} combination does not exist.")
    

    combination_role_screen = UserScreenRole.count_documents({"screen_id": ObjectId(str(screen['screen_id'])), "role_id": ObjectId(str(role['role_id']))})
    
    if(combination_role_screen == 0):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"screen_id , role_id  {screen['screen_id']} {role['role_id']} combination does not exist.")
    
    count_role = UserScreenRole.count_documents({"screen_id": ObjectId(str(screen['screen_id'])), "role_id": ObjectId(str(role['role_id'])) , "link_id": ObjectId(str(link['link_id']))})
    
    if count_role > 0:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"screen_id , role_id,  link_id {screen_id} {role_id} {link_id} already exist.")
    
    UserScreenRole.insert_one({"screen_id": ObjectId(str(screen['screen_id'])), "role_id": ObjectId(str(role['role_id'])), "link_id": ObjectId(str(link['link_id']))})

    return {
        "message": "links to screen assigned successfully",
        "links": content
    }


# Display all links that is assign to login user role autorized links of screen on the base of user login 
@router.post("/screen_for_login_user")
def links_for_screens(link_content: schemas.LinksDisplay ,user= Depends(oauth2.require_user)):
    content = link_content.dict()
    screen_id = content['screen_id']
    user_id = user["id"]
    utils.validate_id(screen_id, None, 'screen_id')    
    users_roles = UsersRoles.find_one({"user_id": ObjectId(str(user_id))})
    
    if(users_roles is None):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"'{user['name']}' You have not a permission to access this page")
    
    
    role = userSerializers.userRole(Role.find_one({"_id" : ObjectId(str(users_roles['role_id']))}))
    
    
    screen = userSerializers.userScreen(Screen.find_one({"_id" : ObjectId(str(screen_id))}))
    
    utils.is_none('screen', screen is None, screen_id)
    
    if(role is None):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"role name '{user['role']}' does not exists")
    
    screens = userSerializers.assignScreens(UserScreenRole.find_one({"role_id": ObjectId(str(role['role_id'])), "screen_id": ObjectId(str(screen['screen_id']))}))
    if screens is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Screen does not exists")
    
    
    links_screens =  list(UserScreenRole.aggregate([{"$match": {"screen_id": ObjectId(str(screens['screen_id'])), "role_id": ObjectId(str(screens['role_id']))}}]))


    links_list = []

    for link in links_screens:
        
        if('link_id' in link):
            links_list += list(Link.aggregate([{"$match": {"screen_id": str(link['screen_id']), "_id":ObjectId(str(link['link_id']))}}]))
        
    if(len(links_list) == 0):

        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Screen links for this Page does not exist")
    
    
    
    return {
        "screen_name": screen['screen_name'],
        "screen_id": screens['screen_id'],
        "screen_allowed_links": links_list
    }



# All links of screen show on the base of role. Autorized screen on the base of user login
@router.post("/link_for_screen")
def link_for_screen(link_content: schemas.LinkDisplay ,user= Depends(oauth2.require_user)):
    
    content = link_content.dict()
    screen_id = content['screen_id']
    link_id = content['link_id']
    user_id = user["id"]

    utils.validate_id(screen_id, None, 'screen_id')
    utils.validate_id(link_id, None, 'link_id') 
    users_roles = UsersRoles.find_one({"user_id": ObjectId(str(user_id))})
    
    if(users_roles is None):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"'{user['name']}' You have not a permission to access this page")
    
    
    role = userSerializers.userRole(Role.find_one({"_id" : ObjectId(str(users_roles['role_id']))}))
    screen = userSerializers.userScreen(Screen.find_one({"_id" : ObjectId(str(screen_id))}))
    link = userSerializers.link_display(Link.find_one({"_id" : ObjectId(str(link_id))}))
    
    utils.is_none('link', link is None, link_id)
    utils.is_none('screen', screen is None, screen_id)
    
    user_role_count = UsersRoles.count_documents({"user_id": ObjectId(str(user['id'])), "role_id": ObjectId(str(role['role_id']))})
    
    if(user_role_count == 0):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"You have not access to see this page")
    
    screens = userSerializers.assignScreens(UserScreenRole.find_one({"role_id": ObjectId(str(role['role_id'])), "screen_id": ObjectId(str(screen['screen_id']))}))

    if not screens:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Screen does not exists")

    
    combination_role_screen_links = UserScreenRole.count_documents({"screen_id": ObjectId(str(screen['screen_id'])), "role_id": ObjectId(str(role['role_id'])), "link_id": ObjectId(str(link['link_id']))})
    
    
    if(combination_role_screen_links == 0):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"{user['name']} attempts to access a webpage that does not exist")
    
    
    user_screen_link = UserScreenRole.find({"screen_id": ObjectId(str(screen['screen_id'])), "role_id": ObjectId(str(role['role_id'])), "link_id": ObjectId(str(link['link_id']))})
    
    
    user_screen_link =  list(UserScreenRole.aggregate([
        {
            "$match": {"screen_id": ObjectId(str(screen['screen_id'])), "role_id": ObjectId(str(role['role_id'])), "link_id": ObjectId(str(link['link_id']))}
        }
    ]))
    
    links_list = []

    
    for link in user_screen_link:
        
        links_list = list(Link.aggregate([{"$match": {"_id": ObjectId(str(link['link_id'])), "screen_id": str(link['screen_id'])}}]))
        
    
    if(len(links_list) == 0):

        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Page doesn't exists")
    
    return {
        "link_content": links_list[0],
    }


# Create Employee
@router.post("/create_employee", status_code=status.HTTP_201_CREATED)
def create_employee(create: schemas.CreateEmployee, user= Depends(oauth2.require_user)):
    try:
        create = create.dict()    
        
        utils.record_exists(Employee, '_id', create['first_name'], 'Employee', None)
        Employee.insert_one(create)
        
        
        return {
            "message": "Employee created successfully...",
            "status": "success"
        }

    except Exception as e:
        error = e.__class__.__name__
        if(error == 'DuplicateKeyError'):
            return {
                "message": "User Already exist",
                "status": "failed"
            }
            
        return {
            "message": "something wrong",
            "status": "failed"   
        }


# All employee belong to application will show
@router.get("/view_employee", response_model=Page[schemas.EmployeeOut])
def employee_list(user= Depends(oauth2.require_user)):
    
    list = [schemas.EmployeeOut(_id = str(i['_id']), first_name = i['first_name'], last_name = i['last_name'], email = i['email'], nick_name = i['nick_name'], department_name = i['department_name'], location_name = i['location_name'], designation = i['designation'], employment_type = i['employment_type'], employee_status = i['employee_status'], date_of_joining = i['date_of_joining']) for i in  Employee.find()]
        
    return  paginate(list)



@router.post("/view_employee_by_id")
def employee_by_id(edit_data: schemas.ViewEditEmployee ,user= Depends(oauth2.require_user)):
    try:
        edit = edit_data.dict()
        employee = userSerializers.employee_dict(Employee.find_one({'_id': ObjectId(str(edit['id']))}))
        return {'status': 'success', "employees": employee}
    except Exception as e:
        print("E=>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", e)


@router.post("/edit_employee_by_id")
# def employee_by_id(edit_data: schemas.CreateEmployee ,user= Depends(oauth2.require_user)):
def employee_by_id(edit_data: schemas.EditEmployee):
    try:
        edit = edit_data.dict()
        print("edit======================================?", edit)
        if('id' not in edit):
            return {
                "message": "id is required",
                "status_code": status.HTTP_400_BAD_REQUEST,
                "status": "failed"
            }
            
        if(edit['id'] is None):
            return {
                "message": "Please enter correct id",
                "status_code": status.HTTP_400_BAD_REQUEST,
                "status": "failed"
            }
            
        utils.validate_id(edit['id'], Employee, "employee_id")
        print("===========================================================================================123", edit['id'])
        try:
            edit_emp = edit
        except:
            pass    
            
        Employee.update_one({"_id": ObjectId(str(edit['id']))}, {'$set': edit_emp})
        # employee = userSerializers.employee_dict(Employee.find_one({'_id': ObjectId(str(edit['id']))}))
        return {'status': 'success'}
    except Exception as e:
        print(e)




@router.delete("/delete_employee_by_id")
def delete_employee_by_id(delete: schemas.ViewEditEmployee ,user= Depends(oauth2.require_user)):
    
    delete = delete.dict()
    if('id' not in delete):
        return {
            "message": "id is required",
            "status_code": status.HTTP_400_BAD_REQUEST,
            "status": "failed"
        }
        
    if(delete['id'] is None):
        return {
            "message": "Please enter correct id",
            "status_code": status.HTTP_400_BAD_REQUEST,
            "status": "failed"
        }
        
    utils.validate_id(delete['id'], Employee, "employee_id")
    
    Employee.delete_one({'_id': ObjectId(str(delete['id']))})
    
    return {'status': 'success', "message": "Employee deleted successfully"}


@router.post("/search_employee")
def search_employee(search: schemas.Search, user= Depends(oauth2.require_user)):
    value = search.dict()
    searching = value['search']
    results =  list(Employee.aggregate([{ "$match": {"$or": [{"first_name": searching}, {"last_name": searching}, {"middle_name": searching},{"department_name": searching}, ]}}]))

    return {
        "items": results
    }