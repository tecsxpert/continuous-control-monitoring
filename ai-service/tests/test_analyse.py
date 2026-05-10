from unittest.mock import patch
def test_analyse_success(client):
    mock_output = '''
    [
        {"type": "risk", "title": "Issue", "description": "Desc", "severity": "high"}
    ]
    '''

    with patch("services.groq_client.generate_response", return_value=mock_output):
        res = client.post("/analyse-document/", json={
            "text": "Some document"
        })

        assert res.status_code == 200
        assert "findings" in res.json
    
def test_analyse_invalid_input(client):
    res = client.post("/analyse-document/", json={})

    assert res.status_code == 400

def test_empty_text(client):
    res = client.post("/analyse-document/", json={"text": ""})

    assert res.status_code == 400