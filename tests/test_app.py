def test_root_redirect(client):
    """Test that root endpoint redirects to static index.html"""
    # Arrange
    # (no setup needed, client is provided by fixture)

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities(client):
    """Test that GET /activities returns all activities with correct structure"""
    # Arrange
    # (no setup needed)

    # Act
    response = client.get("/activities")
    activities = response.json()

    # Assert
    assert response.status_code == 200
    assert len(activities) == 9
    assert "Chess Club" in activities
    assert "participants" in activities["Chess Club"]
    assert "description" in activities["Chess Club"]
    assert "schedule" in activities["Chess Club"]
    assert "max_participants" in activities["Chess Club"]


def test_signup_success(client):
    """Test successful signup adds student to activity participants"""
    # Arrange
    test_email = "newstudent@mergington.edu"
    activity_name = "Chess Club"
    initial_response = client.get("/activities")
    initial_count = len(initial_response.json()[activity_name]["participants"])

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": test_email}
    )

    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]

    # Verify participant was added
    updated_response = client.get("/activities")
    updated_count = len(updated_response.json()[activity_name]["participants"])
    assert updated_count == initial_count + 1
    assert test_email in updated_response.json()[activity_name]["participants"]


def test_unregister_success(client):
    """Test successful unregister removes student from activity participants"""
    # Arrange
    activity_name = "Chess Club"
    activities_response = client.get("/activities")
    participant_to_remove = activities_response.json()[activity_name]["participants"][0]
    initial_count = len(activities_response.json()[activity_name]["participants"])

    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": participant_to_remove}
    )

    # Assert
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]

    # Verify participant was removed
    updated_response = client.get("/activities")
    updated_count = len(updated_response.json()[activity_name]["participants"])
    assert updated_count == initial_count - 1
    assert participant_to_remove not in updated_response.json()[activity_name]["participants"]
