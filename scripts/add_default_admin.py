from ..app.db.dao.userDAO import UserDAO
from ..app.models.user import User

def add_default_admin():
    """
    Adds a default admin user to the database.
    """
    admin = User(
        name="Admin",
        email="admin@admin.com",
        password="admin",
        profile_picture="https://www.gravatar.com/avatar/",
        role="admin",
    )
    user_dao = UserDAO()
    user_dao.add_user(admin)

if __name__ == "__main__":
    add_default_admin()
