import pytest
# from app import app
from app.models import User


# module - run once per module (e.g., a test file)
@pytest.fixture(scope='module') 
def new_user():
    """
    
    """
    user = User(
        email='test@gmail.com', 
        username='test1',
        password='password'
        )
    
    return user