import pytest
@pytest.fixture
def supply_url():
	return "https://reqres.in/api"

@pytest.fixture
def create_user_json():
	return "/JsonFiles/CreateUser.json";
