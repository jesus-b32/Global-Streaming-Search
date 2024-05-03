# import pytest
# from app import app
# from app.models import User



def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email and password_hashed fields are defined correctly
    """
    assert new_user.email == 'test@gmail.com'
    assert new_user.email == 'test1'
    assert new_user.password_hashed != 'FlaskIsAwesome'




# @pytest.fixture
# def client():
#     app.config['TESTING'] = True
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#     with app.test_client() as client:
#         with app.app_context():
#             db.create_all()

#         yield client

#         with app.app_context():
#             db.session.remove()
#             db.close_all_sessions()
#             db.drop_all()