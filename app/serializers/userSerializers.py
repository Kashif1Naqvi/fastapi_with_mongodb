def userEntity(user) -> dict:
    print("user", user)
    if(user is not None):
        return {
            "id": str(user['_id']),
            "name": user['name'],
            "email": user['email'],
            "address": user['address'],
            "verified": user['verified'],
            "password": user['password'],
            "created_at": user['created_at'],
            "updated_at": user['updated_at']
        }

def userResponseEntity(user) -> dict:
    
    return {
        "id": str(user['_id']),
        "name": user['name'],
        "email": user['email'],
        "address": user['address'],
        "created_at": user['created_at'],
        "updated_at": user['updated_at']
    }

def userRole(role):
    if(role):
        return {
            "role_id": str(role['_id']),
            "role_name": role['role_name'],
            "role_description": role['role_description'],
        }

def userScreen(screen):
    print("screen", screen)
    if(screen):
        return {
            "screen_id": str(screen['_id']),
            "screen_name": screen['name'],
            "screen_description": screen['description'],
        }

def assignScreens(screen):
    print("screen->", screen)
    if screen is not None:
        return {
            "role_id": str(screen['role_id']),
            "screen_id": screen['screen_id'],
        }  
    
def rolesassignLinks(link):
    print("link->", link)
    if link is not None:
        return {
            "role_id": str(link['role_id']),
            "link_id": link['link_id'],
        }  
    
def postEntity(post) -> dict:
    print("post", post)
    return {
        "id": str(post["_id"]),
        "title": post["title"],
        "content": post["content"],
        "published": post["published"],
        "user": str(post["user"]),
        "created_at": post["created_at"],
        "updated_at": post["updated_at"]

    }



def link_display(data) -> dict:
    if(data):
        print("data", data)
        return {
            "link_id": data['_id'],
            "screen_id": data['screen_id'],
            "link_text": data['link_text'],
            "link_description": data['link_description'],
        }

# def link_display_list(links) -> list:
#     return [link_display(link) for link in links]


def employee_dict(data) -> dict:
    # print("Data", data)
    
    if(data):
        return {
            "_id": data['_id'],
            "first_name": data['first_name'],
            "last_name": data['last_name'],
            "email": data['email'],
            "nick_name": data['nick_name'],
            "department_name": data['department_name'],
            "location_name": data['location_name'],
            "designation": data['designation'],
            "employment_type": data['employment_type'],
            "employee_status": data['employee_status'],
            "date_of_joining": data['date_of_joining']
        }
