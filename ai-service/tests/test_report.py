from unittest.mock import patch
def test_report_success(client):
    mock_output = '''
    {
        "title": "Report",
        "executive_summary": "Summary",
        "overview": "Overview",
        "top_items": [],
        "recommendations": []
    }
    '''

    with patch("services.groq_client.generate_response", return_value=mock_output):
        res = client.post("/generate-report/", json={
            "title": "Weak password",
            "description": "No rules"
        })

        assert res.status_code == 200
        assert "report" in res.json
    
def test_report_missing_input(client):
    res = client.post("/generate-report/", json={})

    assert res.status_code == 400