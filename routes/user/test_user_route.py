from test.setup import client
from test.utils import validate_response

def test_create_user():
    # Test create user
    response = client.post('/user/', json={'name': 'Test', 'surname': 'User'})
    
    # Validate response
    user = validate_response(response)

    # Validate user data
    assert user['id'] is not None
    assert user['name'] == 'Test'
    assert user['surname'] == 'User'

def test_get_users():
    # Test get users
    response = client.get('/user/')

    # Validate response
    users = validate_response(response)
    assert len(users) == 1

    user = users[0]

    # Validate user data
    assert user['id'] is not None
    assert user['name'] == 'Test'
    assert user['surname'] == 'User'

def test_get_user_by_id():
    # Get all users
    response = client.get('/user/')
    
    # Validate response
    users = validate_response(response)
    assert len(users) == 1

    user_id = users[0]['id']
    assert user_id is not None

    # Get user by id
    response = client.get(f'/user/{user_id}')
    
    # Validate response
    user = validate_response(response)

    # Validate user data
    assert user['id'] is not None
    assert user['name'] == 'Test'
    assert user['surname'] == 'User'

def test_update_user():
    # Get all users
    response = client.get('/user/')

    # Validate response
    users = validate_response(response)
    assert len(users) == 1

    user_id = users[0]['id']
    assert user_id is not None

    # Update user by id
    response = client.put(f'/user/{user_id}', json={'name': 'Test2', 'surname': 'User2'})
    
    # Validate response
    user = validate_response(response)

    # Validate user data
    assert user['id'] is not None
    assert user['name'] == 'Test2'
    assert user['surname'] == 'User2'

def test_patch_user():
    # Get all users
    response = client.get('/user/')
    
    # Validate response
    users = validate_response(response)
    assert len(users) == 1

    user_id = users[0]['id']
    assert user_id is not None

    # Patch user by id
    response = client.patch(f'/user/{user_id}', json={'name': 'Test3'})
    
    # Validate response
    user = validate_response(response)

    # Validate user data
    assert user['id'] is not None
    assert user['name'] == 'Test3'
    assert user['surname'] == 'User2'

def test_delete_user():
    # Get all users
    response = client.get('/user/')
    
    # Validate response
    users = validate_response(response)
    assert len(users) == 1

    user_id = users[0]['id']
    assert user_id is not None
    
    # Delete user by id
    response = client.delete(f'/user/{user_id}')
    
    # Validate response
    deleted = validate_response(response)
    assert deleted is True

    # Check if user has been deleted
    response = client.get('/user/')
    
    # Validate response
    users = validate_response(response)
    assert len(users) == 0
