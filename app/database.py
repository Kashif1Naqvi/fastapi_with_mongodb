from pymongo import mongo_client
import pymongo

from app.config import settings
from bson.objectid import ObjectId

client = mongo_client.MongoClient(
    settings.DATABASE_URL#, ServerSelectionTimeoutMS=5000
)


try:
    conn = client.server_info()
    print(f"Connected with mongo {conn.get('version')}")
except Exception:
    print("Unable to connect with mongo")

    
db = client[settings.MONGO_INITDB_DATABASE]


User = db.user
Screen = db.screen
Link = db.link
Role = db.role
UserScreenRole = db.user_screen_role
UsersRoles = db.users_roles
Employee = db.employee

# UserScreenRole.create_index([("role_id", 1 ), ("screen_id", 1), ("link_id", 1)], unique= True )
UsersRoles.create_index([("user_id", 1 )], unique= True )
Employee.create_index([("email", 1 )], unique= True )

# Post = db.post
# Role = db.role
# RoleUser = db.role_user
# UsersRoles = db.users_roles
# Screen = db.screen
# Link = db.screen_link
# LinksScreens = db.links_screens
# ScreensRoles = db.screens_roles
# LinksUsers = db.links_users

# UserRole = db.user_role

# RolesLinks = db.roles_links

# UserPermission = db.user_permission

User.create_index([("email", pymongo.ASCENDING)], unique=True)

# LinksUsers.create_index([("link_id", 1 )], unique= True )
# RolesLinks.create_index([("link_id", 1 ), ("role_id", 1)], unique= True )