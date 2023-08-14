import pydantic
from fastapi import  status, HTTPException, Depends, APIRouter
from bson.objectid import ObjectId
from .. import schemas, oauth2, utils
from app.serializers import userSerializers
from ..database import User, RoleUser, UsersRoles, Screen, ScreensRoles, User, Link, LinksScreens, LinksUsers, RolesLinks


pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str

router = APIRouter()

#All the roles that is related to users will show here
@router.get('/roles_list')
def roles():
    list = []
    for i in RoleUser.find():
        list.append(i)

    return {'status': 'success', "roles":  list}
    
# All users belong to application will show
@router.get('/users_list')
def users_list():
    list = []
    for i in User.find():
        list.append(i)

    return {'status': 'success', "users":  list}
    
# List of roles assign to users
@router.get('/assign_roles_list')
def assign_roles():
    list = []
    for i in UsersRoles.find():
        list.append(i)

    return {'status': 'success', "assign_roles":  list}

# All screens belong to application will show
@router.get("/list_screen")
def screens_list():
    list = []
    for i in Screen.find():
        list.append(i)

    return {'status': 'success', "screens":  list}

# List of screens assign to users roles
@router.get('/screens_roles_list')
def assign_screens_roles_list():
    list = []
    for i in ScreensRoles.find():
        list.append(i)

    return {'status': 'success', 'message': "Assign roles list", "list":  list}

# All links belong to application will show
@router.get('/screen_links_list')
def screen_links_lists():
    list = []
    for i in Link.find():
        list.append(i)

    return {'status': 'success', 'message': "links lists with every screen id" , "list":  list}

# List of screens assign to links will show
@router.get('/links_screens_relation_list')
def links_screens_relation_list():
    list = []
    for i in LinksScreens.find():
        list.append(i)

    return {'status': 'success', 'message': "Links Belong with screens list" ,"list":  list}



# @router.get('/users_links_list')
# def users_links_list():
#     list = []
#     for i in LinksUsers.find():
#         list.append(i)

#     return {'status': 'success', 'message': "Links Belong with users list" ,"list":  list}

# List of links assign to roles with combinations will show
@router.get('/roles_links_list')
def roles_links_list():
    list = []
    for i in RolesLinks.find():
        list.append(i)

    return {'status': 'success', 'message': "RolesLinks relation list" ,"list":  list}

# Create role for user
@router.post('/create_role')
def create_role(role: schemas.UserRole):
    role_dict = role.dict()    
    
    utils.record_exists(RoleUser, 'role_name', role_dict['role_name'], 'Role')
    
    RoleUser.insert_one(role_dict)
    
    return {
        "Message": "Role created successfully..."
    }


# assign created role to user
@router.post('/assign_roles')
def users_roles_assign(users_roles: schemas.UsersRole):
    # try:
    roles_dict = users_roles.dict()
    print(roles_dict)
    
    if(not utils.check_valid(roles_dict['user_id'])):
        return {
            "Message": "Comma seprated users required"
        }
    
    utils.validate_id(roles_dict["role_id"], None, "role_id")
    
    
    user_ids = roles_dict['user_id'].replace(' ', '').split(',')
    
    utils.is_valid_id(user_ids)
    utils.is_dublicate(user_ids)
    utils.is_exists(User, user_ids)
    
    role = userSerializers.userRole(RoleUser.find_one({"_id" :ObjectId(str(roles_dict['role_id']))}))
    
    print("role", role)
    
    utils.insert_role(role["role_id"], user_ids, UsersRoles, "user_id", "role_id")

    utils.assign_role_to_users(UsersRoles, User, RoleUser)
    
    return {
        "Message": "Roles assign successfully."
    }
    # except Exception as e:
    #     error = e.__class__.__name__
    #     if(error == 'DuplicateKeyError'):
    #         raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail=f"you cannot assign role again to same user")


# create screen e.g Dashboard for users to see when login
@router.post("/create_screen")
def create_screen(screen: schemas.Screen):
    screen_obj = screen.dict()
    value = screen_obj['name']
    utils.record_exists(Screen, 'name', value, 'Screen')
    Screen.insert_one(screen_obj)
    return {
        "Message": "Screen created successfully.",
    }


# Assign created screen for specific user
@router.post("/assign_screens_to_role")
def assign_screens_to_role(screen: schemas.ScreensRoles):
    
    screen_obj = screen.dict()
    role_id = screen_obj['role_id']
    screen_id = screen_obj['screen_id']
    screen_ids = screen_id.replace(' ', '').split(',')
    
    utils.validate_id(role_id, None, "role_id")
    utils.is_valid_id(screen_ids)
    utils.is_dublicate(screen_ids)
    utils.is_exists(Screen, screen_ids)

    role = userSerializers.userRole(RoleUser.find_one({"_id" :ObjectId(str(role_id))}))
    
    utils.insert_role(role["role_id"], screen_ids, ScreensRoles,  "screen_id", "role_id")
    
    return {
        "message": "Assign screens to user role successfully",
        "screen": screen.dict(),
        "role": role
    }


# create links for specific screen e.g Dashboard have links home, service, contact etc 
@router.post("/create_screen_links")
def create_screen_links(links: schemas.CreateScreenLink):
    link = links.dict()
    screen_id = link['screen_id']
    utils.validate_id(screen_id, Screen, 'screen_id')
    utils.record_exists(Link, 'link_text', str(link['link_text']), 'Link')
    Link.insert_one(link)
    return {
        "message": "screen link created successfully",
        "links": link
    }


# Assign links for specifc screen for populating at specific screen
@router.post("/assign_links_screen")
def assign_links_screen(link_content: schemas.LinkContent):
    content = link_content.dict()
    screen_id = content['screen_id']
    link_id = content['link_id']
    utils.validate_id(screen_id, Screen, 'screen_id')
    utils.validate_id(link_id, Link, 'link_id')
    
    count_role = LinksScreens.count_documents({"screen_id": ObjectId(str(screen_id)), "link_id": ObjectId(str(link_id))})

    if count_role > 0:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"screen_id ,link_id {screen_id} {link_id} already exist.")
    
    LinksScreens.insert_one({"screen_id": ObjectId(str(screen_id)), "link_id": ObjectId(str(link_id))})
    return {
        "message": "link for screen created successfully",
        "links": content
    }


# autorized screen on the base of user login
@router.post('/authorized_screens')
def authorized_user_screens(screen: schemas.ScreenPermission ,user= Depends(oauth2.require_user)):
    screen_obj = screen.dict()
    role_name = user['role']
    screen_id = screen_obj['screen_id']
    utils.validate_id(screen_id, None, "screen_id")
    
    role = userSerializers.userRole(RoleUser.find_one({"role_name" : role_name}))
    screen = userSerializers.userScreen(Screen.find_one({"_id" : ObjectId(str(screen_id))}))
    
    # roles_links = RolesLinks.find_one({"role_id": ObjectId(str(role['_id'])),  "link_id": ObjectId(str(link['link_id']))})
    
    # if not roles_links:
    #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"{user['name']} attempts to access a webpage that does not exist")  
    
    
    screens = userSerializers.assignScreens(ScreensRoles.find_one({"role_id": ObjectId(str(role['role_id'])), "screen_id": ObjectId(str(screen['screen_id']))}))
    if not screens:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Screen does not exists")
   
    return {
        "message": f"Welcome {user['name']} your Role is {role_name}",
        "screens": screens,
        "screen_info": screen,
        "login_user_info": user
    }

# Display all links that is assign to login user role autorized links of screen on the base of user login 
@router.post("/links_for_screens")
def links_for_screens(link_content: schemas.LinksDisplay ,user= Depends(oauth2.require_user)):
    content = link_content.dict()
    screen_id = content['screen_id']
    role_name = user['role']

    utils.validate_id(screen_id, None, 'screen_id')    
    role = userSerializers.userRole(RoleUser.find_one({"role_name" : role_name}))
    
    screen = userSerializers.userScreen(Screen.find_one({"_id" : ObjectId(str(screen_id))}))
    
    screens = userSerializers.assignScreens(ScreensRoles.find_one({"role_id": ObjectId(str(role['role_id'])), "screen_id": ObjectId(str(screen['screen_id']))}))

    if not screens:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Screen does not exists")
   
    links_screens =  list(LinksScreens.aggregate([{"$match": {"screen_id": ObjectId(str(screens['screen_id']))}}]))
    

    links_list = []

    for link in links_screens:

        roles_links = RolesLinks.find_one({"role_id": ObjectId(str(screens['role_id'])), "link_id": ObjectId(str(link['link_id']))})

        if roles_links is not None:

            links_list += list(Link.aggregate([{"$match": {"screen_id": str(link['screen_id']), "_id": ObjectId(str(roles_links['link_id']))}}]))

    if(len(links_list) == 0):

        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Page doesn't exists")
    
    return {
        "message": f"Links List at screen_id {screen_id}",
        "links": links_list,
        "screens": screens
    }
    

# @router.post("/assign_to_users_links")
# def users_links(payload: schemas.LinksUsers):
#     content = payload.dict()
#     screen_id = content['screen_id']
#     link_id = content['link_id']
#     user_id = content['user_id']

#     utils.validate_id(user_id, None, 'user_id')
#     utils.validate_id(screen_id, None, 'screen_id')
#     utils.validate_id(link_id, None, 'link_id') 
    
#     user = User.find_one({"_id": ObjectId(str(user_id))})
#     role_name = user['role']
#     print("user role", role_name) 
    # role = userSerializers.userRole(RoleUser.find_one({"role_name" : role_name}))
    # screen = userSerializers.userScreen(Screen.find_one({"_id" : ObjectId(str(screen_id))}))
    
    # utils.is_none('screen_id', screen is None, screen_id)
    # utils.is_none('role', role is None, role_name)

#     screens = userSerializers.assignScreens(ScreensRoles.find_one({"role_id": ObjectId(str(role['role_id'])), "screen_id": ObjectId(str(screen['screen_id']))}))

#     if not screens:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Screen does not exists")
   
#     link_screens =  list(LinksScreens.aggregate([
#         {
#             "$match": {"screen_id": ObjectId(str(screens['screen_id'])), 'link_id': ObjectId(str(link_id))}
#         }
#     ]))
#     links_users = LinksUsers.count_documents({"screen_id": ObjectId(str(screen['screen_id'])), "link_id": ObjectId(str(link_id)), "user_id": ObjectId(str(user['_id']))})

#     if links_users > 0:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"screen_id ,link_id, user_id {screen_id} {link_id} {user_id} already exist.")
    
#     LinksUsers.insert_one({"screen_id": ObjectId(str(screen['screen_id'])), "link_id": ObjectId(str(link_id)), "user_id": ObjectId(str(user['_id']))})
    
#     return {
#         "message": "Link for user added successfully",
#     }



# Assign user role to link combination, combination of one role and one link only allowed
@router.post("/assign_to_roles_links")
def roles_links(payload: schemas.RolesLinks):
    content = payload.dict()
    role_id = content['role_id']
    link_id = content['link_id']

    utils.validate_id(role_id, None, 'role_id')
    utils.validate_id(link_id, None, 'link_id') 
    
    role = userSerializers.userRole(RoleUser.find_one({"_id" : ObjectId(str(role_id))}))
    link = userSerializers.link_display(Link.find_one({"_id" : ObjectId(str(link_id))}))
    
    utils.is_none('link_id', link is None, link_id)
    utils.is_none('role', role is None, role_id)

    
    RolesLinks.insert_one({"role_id": ObjectId(str(role['role_id'])), "link_id": ObjectId(str(link['link_id']))})
    
    return {
        "message": "roles links relation added successfully",
    }


# All links of screen show on the base of role. Autorized screen on the base of user login
@router.post("/link_for_screen")
def link_for_screen(link_content: schemas.LinkDisplay ,user= Depends(oauth2.require_user)):
    content = link_content.dict()
    screen_id = content['screen_id']
    link_id = content['link_id']
    role_name = user['role']    

    utils.validate_id(screen_id, None, 'screen_id')
    utils.validate_id(link_id, None, 'link_id') 
    utils.validate_id(user['id'], None, 'user_id') 
    
    role = userSerializers.userRole(RoleUser.find_one({"role_name" : role_name}))
    screen = userSerializers.userScreen(Screen.find_one({"_id" : ObjectId(str(screen_id))}))
    link = userSerializers.link_display(Link.find_one({"_id" : ObjectId(str(link_id))}))

    utils.is_none('link', link is None, link_id)
    utils.is_none('screen', screen is None, screen_id)
    utils.is_none('role', role is None, role['role_id'])
    
    screens = userSerializers.assignScreens(ScreensRoles.find_one({"role_id": ObjectId(str(role['role_id'])), "screen_id": ObjectId(str(screen['screen_id']))}))

    if not screens:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Screen does not exists")
    
    roles_links = RolesLinks.find_one({"role_id": ObjectId(str(screens['role_id'])),  "link_id": ObjectId(str(link['link_id']))})
    
    if not roles_links:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"{user['name']} attempts to access a webpage that does not exist")  
    
    link_screens =  list(LinksScreens.aggregate([
        {
            "$match": {"screen_id": ObjectId(str(screens['screen_id'])), 'link_id': ObjectId(str(roles_links['link_id']))}
        }
    ]))

    links_list = []

    for link in link_screens:
        
        links_list = list(Link.aggregate([{"$match": {"_id": ObjectId(str(link['link_id'])), "screen_id": str(link['screen_id'])}}]))
        
    if(len(links_list) == 0):

        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Page doesn't exists")
    
    return {
        "message": f"Links List at screen_id {screen_id}",
        "links": links_list[0],
    }
    

