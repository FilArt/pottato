from httpx import AsyncClient
import json

from pottato.views.user import UserSchema


async def test_create_user(client: AsyncClient):
    """Test creating a new user."""
    user_data = {"email": "test@example.com", "full_name": "Test User"}
    response = await client.post("/user/create-user", json=user_data)
    assert response.status_code == 200
    created_user = UserSchema.model_validate_json(response.content)  # Use model_validate_json
    assert created_user.email == "test@example.com"
    assert created_user.full_name == "Test User"
    assert created_user.id is not None


async def test_get_user(client: AsyncClient):
    """Test retrieving a user by ID."""
    # First, create a user.
    user_data = {"email": "test@example.com", "full_name": "Test User"}
    response = await client.post("/user/create-user", json=user_data)
    assert response.status_code == 200
    created_user = UserSchema.model_validate_json(response.content)
    user_id = created_user.id

    # Now, retrieve the user by ID.
    response = await client.get(f"/user/get-user?id={user_id}")
    assert response.status_code == 200
    retrieved_user = UserSchema.model_validate_json(response.content)
    assert retrieved_user.id == user_id
    assert retrieved_user.email == "test@example.com"
    assert retrieved_user.full_name == "Test User"


async def test_get_user_404(client: AsyncClient):
    """Test retrieving a non-existent user."""
    response = await client.get("/user/get-user?id=nonexistent")
    assert response.status_code == 404


async def test_get_users(client: AsyncClient):
    """Test retrieving all users."""
    # Create two users first
    user_data1 = {"email": "test1@example.com", "full_name": "Test User 1"}
    response1 = await client.post("/user/create-user", json=user_data1)
    assert response1.status_code == 200
    user_data2 = {"email": "test2@example.com", "full_name": "Test User 2"}
    response2 = await client.post("/user/create-user", json=user_data2)
    assert response2.status_code == 200

    # Get all users
    response = await client.get("/user/get-users")
    assert response.status_code == 200
    users = [UserSchema.model_validate_json(json.dumps(user)) for user in response.json()]
    assert len(users) >= 2  # Ensure we have at least 2 created users

    emails = {user.email for user in users}
    assert "test1@example.com" in emails
    assert "test2@example.com" in emails
