import pytest


class TestGetCategoryComparison:
    def test_category_not_found(self, client):
        """测试分类不存在返回404"""
        response = client.get("/api/categories/unknown/comparison")
        assert response.status_code == 404
        data = response.json()
        assert data["error"]["code"] == "CATEGORY_NOT_FOUND"

    def test_get_category_comparison(self, client, seed_data):
        """测试获取分类价格对比"""
        response = client.get("/api/categories/dining/comparison")
        assert response.status_code == 200
        data = response.json()

        assert data["category"] == "dining"
        assert data["categoryName"] == "餐饮"
        assert len(data["items"]) == 2

        first_item = data["items"][0]
        assert first_item["name"] == "平价餐厅一顿饭"
        assert "beijing" in first_item["prices"]
        assert "shanghai" in first_item["prices"]
        assert first_item["prices"]["beijing"] == 40
        assert first_item["prices"]["shanghai"] == 38
        assert first_item["min"] == 38
        assert first_item["max"] == 40
