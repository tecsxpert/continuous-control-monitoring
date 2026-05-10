from unittest.mock import patch

def test_describe_success(client):
    mock_response = "Professional audit description."

    with patch("services.groq_client.generate_response", return_value=mock_response):
        res = client.post("/describe/", json={
            "title": "Weak password",
            "description": "No complexity"
        })

        assert res.status_code == 200
        assert "description" in res.json
    
def test_describe_invalid_input(client):
    res = client.post("/describe/", json={})

    assert res.status_code == 400