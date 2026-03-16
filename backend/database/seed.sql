-- ============================================
-- 城市生活成本查询系统 - 初始数据
-- 基于 data.js 生成
-- ============================================

SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- ============================================
-- 1. 插入城市数据
-- ============================================
INSERT INTO cities (city_key, name, emoji, center_def) VALUES
('beijing', '北京', '🏛️', '三环内'),
('shanghai', '上海', '🌆', '内环内'),
('shenzhen', '深圳', '🏙️', '福田/南山核心区'),
('guangzhou', '广州', '🌺', '天河/越秀核心区');

-- ============================================
-- 2. 插入分类数据
-- ============================================
INSERT INTO categories (category_key, name, icon, sort_order) VALUES
('dining', '餐饮', '🥗', 1),
('market', '超市/市场', '🛒', 2),
('transport', '交通', '🚗', 3),
('utilities', '生活杂费', '⚡', 4),
('leisure', '运动与休闲', '🏸', 5),
('clothing', '服装', '👕', 6),
('housing', '租房', '🏠', 7),
('salary', '薪资与购房', '💰', 8);

-- ============================================
-- 3. 插入价格项目数据
-- ============================================

-- 餐饮 (dining)
INSERT INTO items (category_key, name, description, unit, is_big_price, is_salary, sort_order) VALUES
('dining', '平价餐厅一顿饭', '普通快餐/盖浇饭/工作餐', '元', FALSE, FALSE, 1),
('dining', '中档餐厅两人餐', '三道菜，如海底捞等', '元', FALSE, FALSE, 2),
('dining', '麦当劳套餐', '标准化价格参考', '元', FALSE, FALSE, 3),
('dining', '咖啡（常规）', '星巴克/瑞幸', '元', FALSE, FALSE, 4),
('dining', '饮料 (330ml)', '', '元', FALSE, FALSE, 5),
('dining', '瓶装水 (330ml)', '', '元', FALSE, FALSE, 6);

-- 超市/市场 (market)
INSERT INTO items (category_key, name, description, unit, is_big_price, is_salary, sort_order) VALUES
('market', '牛奶 (1L)', '', '元', FALSE, FALSE, 1),
('market', '大米 (1kg)', '', '元', FALSE, FALSE, 2),
('market', '鸡蛋 (12个)', '', '元', FALSE, FALSE, 3),
('market', '猪肉 (1kg)', '', '元', FALSE, FALSE, 4),
('market', '鸡胸肉 (1kg)', '', '元', FALSE, FALSE, 5),
('market', '牛肉 (1kg)', '牛腿肉/适合炒菜', '元', FALSE, FALSE, 6),
('market', '苹果 (1kg)', '', '元', FALSE, FALSE, 7),
('market', '香蕉 (1kg)', '', '元', FALSE, FALSE, 8),
('market', '橙子 (1kg)', '', '元', FALSE, FALSE, 9),
('market', '番茄 (1kg)', '', '元', FALSE, FALSE, 10),
('market', '土豆 (1kg)', '', '元', FALSE, FALSE, 11),
('market', '洋葱 (1kg)', '', '元', FALSE, FALSE, 12),
('market', '青菜/绿叶菜 (1kg)', '', '元', FALSE, FALSE, 13),
('market', '瓶装水 (1.5L)', '', '元', FALSE, FALSE, 14);

-- 交通 (transport)
INSERT INTO items (category_key, name, description, unit, is_big_price, is_salary, sort_order) VALUES
('transport', '单程车票（公交/地铁）', '', '元', FALSE, FALSE, 1),
('transport', '出租车起步价', '含网约车参考', '元', FALSE, FALSE, 2),
('transport', '出租车 1km 计费', '', '元', FALSE, FALSE, 3),
('transport', '出租车等候 (1小时)', '', '元', FALSE, FALSE, 4),
('transport', '汽油 (1L)', '', '元', FALSE, FALSE, 5),
('transport', '购车（大众Golf）', '中型燃油车参考', '元', TRUE, FALSE, 6),
('transport', '购车（特斯拉Model 3）', '电车参考', '元', TRUE, FALSE, 7);

-- 生活杂费 (utilities)
INSERT INTO items (category_key, name, description, unit, is_big_price, is_salary, sort_order) VALUES
('utilities', '基础水电煤 (85平米)', '电费+水费+燃气+物业', '元/月', FALSE, FALSE, 1),
('utilities', '手机套餐 (30GB+)', '三大运营商5G套餐', '元/月', FALSE, FALSE, 2),
('utilities', '宽带 (300Mbps+)', '', '元/月', FALSE, FALSE, 3);

-- 运动与休闲 (leisure)
INSERT INTO items (category_key, name, description, unit, is_big_price, is_salary, sort_order) VALUES
('leisure', '健身房月卡', '', '元/月', FALSE, FALSE, 1),
('leisure', '羽毛球场 (1小时/周末)', '', '元', FALSE, FALSE, 2),
('leisure', '电影票', '', '元', FALSE, FALSE, 3);

-- 服装 (clothing)
INSERT INTO items (category_key, name, description, unit, is_big_price, is_salary, sort_order) VALUES
('clothing', '牛仔裤', '', '元', FALSE, FALSE, 1),
('clothing', '上衣 (Zara/H&M/优衣库)', '', '元', FALSE, FALSE, 2),
('clothing', '运动鞋 (安踏/耐克)', '', '元', FALSE, FALSE, 3);

-- 租房 (housing)
INSERT INTO items (category_key, name, description, unit, is_big_price, is_salary, sort_order) VALUES
('housing', '市中心一居室', '', '元/月', FALSE, FALSE, 1),
('housing', '非市中心一居室', '', '元/月', FALSE, FALSE, 2),
('housing', '市中心三居室', '', '元/月', FALSE, FALSE, 3),
('housing', '非市中心三居室', '', '元/月', FALSE, FALSE, 4);

-- 薪资与购房 (salary)
INSERT INTO items (category_key, name, description, unit, is_big_price, is_salary, sort_order) VALUES
('salary', '市中心房价 (每平米)', '', '元', TRUE, FALSE, 1),
('salary', '非市中心房价 (每平米)', '', '元', TRUE, FALSE, 2),
('salary', '税后平均月薪', '', '元', FALSE, TRUE, 3);

-- ============================================
-- 4. 插入城市价格数据
-- ============================================

-- 北京价格数据
INSERT INTO city_prices (city_key, item_id, price)
SELECT 'beijing', id, price FROM (
    SELECT 1 as id, 40 as price UNION ALL
    SELECT 2, 320 UNION ALL
    SELECT 3, 42 UNION ALL
    SELECT 4, 30 UNION ALL
    SELECT 5, 6 UNION ALL
    SELECT 6, 2.5 UNION ALL
    SELECT 7, 14 UNION ALL
    SELECT 8, 8 UNION ALL
    SELECT 9, 16 UNION ALL
    SELECT 10, 32 UNION ALL
    SELECT 11, 26 UNION ALL
    SELECT 12, 78 UNION ALL
    SELECT 13, 13 UNION ALL
    SELECT 14, 8 UNION ALL
    SELECT 15, 11 UNION ALL
    SELECT 16, 10 UNION ALL
    SELECT 17, 6 UNION ALL
    SELECT 18, 6.5 UNION ALL
    SELECT 19, 8 UNION ALL
    SELECT 20, 4 UNION ALL
    SELECT 21, 5 UNION ALL
    SELECT 22, 13 UNION ALL
    SELECT 23, 2.3 UNION ALL
    SELECT 24, 54 UNION ALL
    SELECT 25, 8.2 UNION ALL
    SELECT 26, 148000 UNION ALL
    SELECT 27, 245900 UNION ALL
    SELECT 28, 680 UNION ALL
    SELECT 29, 148 UNION ALL
    SELECT 30, 100 UNION ALL
    SELECT 31, 350 UNION ALL
    SELECT 32, 80 UNION ALL
    SELECT 33, 50 UNION ALL
    SELECT 34, 420 UNION ALL
    SELECT 35, 220 UNION ALL
    SELECT 36, 620 UNION ALL
    SELECT 37, 6800 UNION ALL
    SELECT 38, 3600 UNION ALL
    SELECT 39, 15000 UNION ALL
    SELECT 40, 7200 UNION ALL
    SELECT 41, 95000 UNION ALL
    SELECT 42, 42000 UNION ALL
    SELECT 43, 12500
) AS beijing_prices;

-- 上海价格数据
INSERT INTO city_prices (city_key, item_id, price)
SELECT 'shanghai', id, price FROM (
    SELECT 1 as id, 38 as price UNION ALL
    SELECT 2, 300 UNION ALL
    SELECT 3, 42 UNION ALL
    SELECT 4, 28 UNION ALL
    SELECT 5, 6 UNION ALL
    SELECT 6, 2.5 UNION ALL
    SELECT 7, 13.5 UNION ALL
    SELECT 8, 7.5 UNION ALL
    SELECT 9, 15 UNION ALL
    SELECT 10, 30 UNION ALL
    SELECT 11, 24 UNION ALL
    SELECT 12, 75 UNION ALL
    SELECT 13, 12 UNION ALL
    SELECT 14, 7.5 UNION ALL
    SELECT 15, 10 UNION ALL
    SELECT 16, 9 UNION ALL
    SELECT 17, 5.5 UNION ALL
    SELECT 18, 6 UNION ALL
    SELECT 19, 7 UNION ALL
    SELECT 20, 3.5 UNION ALL
    SELECT 21, 4 UNION ALL
    SELECT 22, 14 UNION ALL
    SELECT 23, 2.5 UNION ALL
    SELECT 24, 57 UNION ALL
    SELECT 25, 8.5 UNION ALL
    SELECT 26, 148000 UNION ALL
    SELECT 27, 245900 UNION ALL
    SELECT 28, 650 UNION ALL
    SELECT 29, 148 UNION ALL
    SELECT 30, 90 UNION ALL
    SELECT 31, 320 UNION ALL
    SELECT 32, 75 UNION ALL
    SELECT 33, 48 UNION ALL
    SELECT 34, 400 UNION ALL
    SELECT 35, 210 UNION ALL
    SELECT 36, 600 UNION ALL
    SELECT 37, 6500 UNION ALL
    SELECT 38, 3400 UNION ALL
    SELECT 39, 14000 UNION ALL
    SELECT 40, 6800 UNION ALL
    SELECT 41, 98000 UNION ALL
    SELECT 42, 45000 UNION ALL
    SELECT 43, 12800
) AS shanghai_prices;

-- 深圳价格数据
INSERT INTO city_prices (city_key, item_id, price)
SELECT 'shenzhen', id, price FROM (
    SELECT 1 as id, 35 as price UNION ALL
    SELECT 2, 280 UNION ALL
    SELECT 3, 40 UNION ALL
    SELECT 4, 28 UNION ALL
    SELECT 5, 5.5 UNION ALL
    SELECT 6, 2 UNION ALL
    SELECT 7, 13 UNION ALL
    SELECT 8, 7 UNION ALL
    SELECT 9, 14 UNION ALL
    SELECT 10, 28 UNION ALL
    SELECT 11, 22 UNION ALL
    SELECT 12, 72 UNION ALL
    SELECT 13, 11 UNION ALL
    SELECT 14, 7 UNION ALL
    SELECT 15, 9.5 UNION ALL
    SELECT 16, 8.5 UNION ALL
    SELECT 17, 5 UNION ALL
    SELECT 18, 5.5 UNION ALL
    SELECT 19, 6.5 UNION ALL
    SELECT 20, 3.5 UNION ALL
    SELECT 21, 4 UNION ALL
    SELECT 22, 11 UNION ALL
    SELECT 23, 2.4 UNION ALL
    SELECT 24, 50 UNION ALL
    SELECT 25, 8.0 UNION ALL
    SELECT 26, 145000 UNION ALL
    SELECT 27, 245900 UNION ALL
    SELECT 28, 620 UNION ALL
    SELECT 29, 128 UNION ALL
    SELECT 30, 80 UNION ALL
    SELECT 31, 300 UNION ALL
    SELECT 32, 70 UNION ALL
    SELECT 33, 45 UNION ALL
    SELECT 34, 380 UNION ALL
    SELECT 35, 200 UNION ALL
    SELECT 36, 580 UNION ALL
    SELECT 37, 5800 UNION ALL
    SELECT 38, 2800 UNION ALL
    SELECT 39, 13000 UNION ALL
    SELECT 40, 5500 UNION ALL
    SELECT 41, 88000 UNION ALL
    SELECT 42, 38000 UNION ALL
    SELECT 43, 11500
) AS shenzhen_prices;

-- 广州价格数据
INSERT INTO city_prices (city_key, item_id, price)
SELECT 'guangzhou', id, price FROM (
    SELECT 1 as id, 30 as price UNION ALL
    SELECT 2, 250 UNION ALL
    SELECT 3, 38 UNION ALL
    SELECT 4, 26 UNION ALL
    SELECT 5, 5 UNION ALL
    SELECT 6, 2 UNION ALL
    SELECT 7, 12.5 UNION ALL
    SELECT 8, 6.5 UNION ALL
    SELECT 9, 13 UNION ALL
    SELECT 10, 26 UNION ALL
    SELECT 11, 20 UNION ALL
    SELECT 12, 68 UNION ALL
    SELECT 13, 10 UNION ALL
    SELECT 14, 6.5 UNION ALL
    SELECT 15, 9 UNION ALL
    SELECT 16, 8 UNION ALL
    SELECT 17, 4.5 UNION ALL
    SELECT 18, 5 UNION ALL
    SELECT 19, 6 UNION ALL
    SELECT 20, 3 UNION ALL
    SELECT 21, 3 UNION ALL
    SELECT 22, 12 UNION ALL
    SELECT 23, 2.6 UNION ALL
    SELECT 24, 48 UNION ALL
    SELECT 25, 7.8 UNION ALL
    SELECT 26, 145000 UNION ALL
    SELECT 27, 245900 UNION ALL
    SELECT 28, 580 UNION ALL
    SELECT 29, 128 UNION ALL
    SELECT 30, 80 UNION ALL
    SELECT 31, 250 UNION ALL
    SELECT 32, 60 UNION ALL
    SELECT 33, 42 UNION ALL
    SELECT 34, 350 UNION ALL
    SELECT 35, 190 UNION ALL
    SELECT 36, 550 UNION ALL
    SELECT 37, 4500 UNION ALL
    SELECT 38, 2200 UNION ALL
    SELECT 39, 9500 UNION ALL
    SELECT 40, 4500 UNION ALL
    SELECT 41, 65000 UNION ALL
    SELECT 42, 28000 UNION ALL
    SELECT 43, 10200
) AS guangzhou_prices;

-- ============================================
-- 5. 插入月度预估数据
-- ============================================
INSERT INTO monthly_estimates (city_key, single_estimate) VALUES
('beijing', 8500),
('shanghai', 8200),
('shenzhen', 7500),
('guangzhou', 6200);
