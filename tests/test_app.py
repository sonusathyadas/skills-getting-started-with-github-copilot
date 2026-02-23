import src.app as app_module


# ---------------------------------------------------------------------------
# GET /
# ---------------------------------------------------------------------------

class TestRoot:
    def test_redirects_to_index(self, client):
        # Arrange
        # (no preconditions — the root route always redirects)

        # Act
        response = client.get("/")

        # Assert
        assert response.status_code in (301, 302, 307, 308)
        assert response.headers["location"] == "/static/index.html"


# ---------------------------------------------------------------------------
# GET /activities
# ---------------------------------------------------------------------------

class TestGetActivities:
    def test_returns_all_activities(self, client):
        # Arrange
        # (activities are pre-seeded in the app; no extra setup required)

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) > 0

    def test_known_activity_has_expected_fields(self, client):
        # Arrange
        expected_fields = {"description", "schedule", "max_participants", "participants"}

        # Act
        response = client.get("/activities")

        # Assert
        data = response.json()
        assert "Chess Club" in data
        assert expected_fields.issubset(data["Chess Club"].keys())


# ---------------------------------------------------------------------------
# POST /activities/{activity_name}/signup
# ---------------------------------------------------------------------------

class TestSignup:
    def test_signup_success(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 200
        assert email in app_module.activities[activity_name]["participants"]

    def test_signup_unknown_activity_returns_404(self, client):
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 404

    def test_signup_duplicate_email_returns_400(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "duplicate@mergington.edu"
        app_module.activities[activity_name]["participants"].append(email)

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 400


# ---------------------------------------------------------------------------
# DELETE /activities/{activity_name}/signup
# ---------------------------------------------------------------------------

class TestUnregister:
    def test_unregister_success(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "toremove@mergington.edu"
        app_module.activities[activity_name]["participants"].append(email)

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 200
        assert email not in app_module.activities[activity_name]["participants"]

    def test_unregister_unknown_activity_returns_404(self, client):
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 404

    def test_unregister_student_not_enrolled_returns_404(self, client):
        # Arrange
        activity_name = "Chess Club"
        email = "notregistered@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 404
