from app.modules.domain.user import User


def test_init_user(db_user):
    user = User(email="test@gmail.com")
    assert user != None

    user_by_id = User(id=user.get_id())
    assert user_by_id != None


def test_init_failed(db_user):
    try:
        user = User(id="12345")
        assert True == False
    except Exception:
        pass

    try:
        user = User()
        assert True == False
    except Exception:
        pass


def test_create_user(db):
    user = User.create(
        email="test@gmail.com",
        name="User1",
        password="test",
        role="Admin",
        image="",
        introduction=""
    )
    assert user.get_name() == "User1"


def test_get_all(db_user):
    user = User(email="test@gmail.com")
    assert len(user.get_all()) == 2


def test_get(db_user):
    user = User(email="test@gmail.com")
    assert user.get().name == 'User1'

    assert user.get_email() == "test@gmail.com"
    assert user.get_image() == ""
    assert user.get_introduction() == ""
    assert len(user.get_id()) == 24
    assert user.get_password() != None
    assert user.get_urole() == "Admin"
    assert user.is_authenticated() == True
    assert user.is_active() == True
    assert user.is_anonymous() == False


def test_delete(db_user):
    user = User(email="test@gmail.com")
    user.delete()
    try:
        user = User(email="test@gmail.com")
        assert True == False
    except Exception:
        pass


def test_update_role(db_user):
    user = User(email="test@gmail.com")
    user.update_role("Nurse")

    assert user.get_urole() == "Nurse"

    user.update_role("Admin")
    assert user.get_urole() == "Admin"

    try:
        user.update_role("awer")
        assert True == False
    except Exception:
        pass
