import pytest


class TestCompare:
    def test_compare_requires_two_cities(self, client):
        """测试至少需要2个城市"""
        response = client.get("/api/compare?cities=beijing")
        assert response.status_code == 400
        data = response.json()
        assert data["error"]["code"] == "INVALID_PARAMS"

    def test_compare_invalid_cities(self, client):
        """测试无效城市"""
        response = client.get("/api/compare?cities=unknown1,unknown2")
        assert response.status_code == 400

    def test_compare_cities(self, client, seed_data):
        """测试多城市对比"""
        response = client.get("/api/compare?cities=beijing,shanghai")
        assert response.status_code == 200
        data = response.json()

        assert set(data["cities"]) == {"beijing", "shanghai"}
        assert "comparison" in data

        comparison = data["comparison"]
        assert "monthlyEstimate" in comparison
        assert comparison["monthlyEstimate"]["beijing"]["single"] == 8500
        assert comparison["monthlyEstimate"]["shanghai"]["single"] == 8200

        assert "centerDef" in comparison
        assert comparison["centerDef"]["beijing"] == "三环内"
        assert comparison["centerDef"]["shanghai"] == "内环内"

        assert "categories" in comparison
        assert "dining" in comparison["categories"]
