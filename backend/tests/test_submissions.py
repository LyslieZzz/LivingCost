import pytest


class TestSubmissions:
    """测试预留的用户提交接口"""

    def test_create_submission_not_implemented(self, client):
        """测试提交接口返回501"""
        response = client.post(
            "/api/submissions",
            json={
                "city_key": "beijing",
                "item_id": 1,
                "submitted_price": 35.5,
                "source_desc": "测试来源",
            },
        )
        assert response.status_code == 501
        data = response.json()
        assert data["error"]["code"] == "NOT_IMPLEMENTED"

    def test_list_submissions_not_implemented(self, client):
        """测试列表接口返回501"""
        response = client.get("/api/submissions")
        assert response.status_code == 501

    def test_review_submission_not_implemented(self, client):
        """测试审核接口返回501"""
        response = client.patch(
            "/api/submissions/1",
            json={"status": "approved", "reviewer_note": "通过"},
        )
        assert response.status_code == 501
