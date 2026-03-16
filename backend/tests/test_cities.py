import pytest


class TestGetCities:
    def test_get_cities_empty(self, client):
        """测试空数据库返回空列表"""
        response = client.get("/api/cities")
        assert response.status_code == 200
        data = response.json()
        assert "cities" in data
        assert data["cities"] == []

    def test_get_cities_with_data(self, client, seed_data):
        """测试返回城市列表"""
        response = client.get("/api/cities")
        assert response.status_code == 200
        data = response.json()
        assert len(data["cities"]) == 2

        beijing = next((c for c in data["cities"] if c["key"] == "beijing"), None)
        assert beijing is not None
        assert beijing["name"] == "北京"
        assert beijing["emoji"] == "🏛️"
        assert beijing["centerDef"] == "三环内"


class TestGetCityCosts:
    def test_city_not_found(self, client):
        """测试城市不存在返回404"""
        response = client.get("/api/cities/unknown/costs")
        assert response.status_code == 404
        data = response.json()
        assert data["error"]["code"] == "CITY_NOT_FOUND"

    def test_get_city_costs(self, client, seed_data):
        """测试获取城市生活成本详情"""
        response = client.get("/api/cities/beijing/costs")
        assert response.status_code == 200
        data = response.json()

        assert data["city"]["key"] == "beijing"
        assert data["city"]["name"] == "北京"
        assert data["monthlyEstimate"]["single"] == 8500

        assert "dining" in data["categories"]
        assert len(data["categories"]["dining"]["items"]) == 2
        assert data["categories"]["dining"]["items"][0]["name"] == "平价餐厅一顿饭"
        assert data["categories"]["dining"]["items"][0]["price"] == 40


class TestGetCityEstimate:
    def test_city_not_found(self, client):
        """测试城市不存在返回404"""
        response = client.get("/api/cities/unknown/estimate")
        assert response.status_code == 404

    def test_get_city_estimate(self, client, seed_data):
        """测试获取城市月度预估"""
        response = client.get("/api/cities/beijing/estimate")
        assert response.status_code == 200
        data = response.json()

        assert data["cityKey"] == "beijing"
        assert data["cityName"] == "北京"
        assert data["estimate"]["single"] == 8500
