from auth import register_user, login_user

def test_registration():
    print("Testing user registration...")
    
    # Test user data
    test_user = {
        "name": "Test User",
        "username": "testuser",
        "password": "testpass123",
        "email": "test@example.com",
        "location": "Test City"
    }
    
    # Try to register
    response, status = register_user(
        test_user["name"],
        test_user["username"],
        test_user["password"],
        test_user["email"],
        test_user["location"]
    )
    
    print(f"Registration Status: {status}")
    print(f"Response: {response}")
    
    if status == 200:
        print("\nTesting login...")
        login_response, login_status = login_user(test_user["username"], test_user["password"])
        print(f"Login Status: {login_status}")
        print(f"Login Response: {login_response}")

if __name__ == "__main__":
    test_registration() 