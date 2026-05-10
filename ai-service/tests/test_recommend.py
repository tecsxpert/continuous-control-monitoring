from unittest.mock import patch

def test_recommend_success(client):
    mock_output = '''
    [
        {"action_type": "policy", "description": "Fix", "priority": "high"},
        {"action_type": "technical", "description": "Fix2", "priority": "medium"},
        {"action_type": "monitoring", "description": "Fix3", "priority": "low"}
    ]
    '''

    with patch("services.groq_client.generate_response", return_value=mock_output):
        res = client.post("/recommend/", json={
            "title": "Weak password",
            "description": "No rules"
        })

        assert res.status_code == 200
        assert "recommendations" in res.json
    
def test_recommend_invalid_json(client):
    with patch("routes.recommend.generate_response", return_value="invalid"):
        res = client.post("/recommend/", json={
            "title": "test",
            "description": "test"
        })

        assert res.status_code == 500