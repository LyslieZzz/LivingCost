-- ============================================
-- 城市生活成本查询系统 - API 查询示例
-- 对应 API 文档中的各个接口
-- ============================================

-- ============================================
-- API 1: GET /api/cities
-- 获取支持的城市列表
-- ============================================
SELECT 
    city_key AS `key`,
    name,
    emoji,
    center_def AS centerDef
FROM cities
ORDER BY city_key;

-- ============================================
-- API 2: GET /api/cities/{cityKey}/costs
-- 获取指定城市的完整生活成本数据
-- 示例: cityKey = 'beijing'
-- ============================================

-- 获取城市基本信息
SELECT 
    city_key AS `key`,
    name,
    center_def AS centerDef,
    emoji
FROM cities
WHERE city_key = 'beijing';

-- 获取城市月度预估
SELECT single_estimate AS single
FROM monthly_estimates
WHERE city_key = 'beijing';

-- 获取城市所有分类及价格项目
SELECT 
    c.category_key,
    c.name AS category_name,
    c.icon AS category_icon,
    i.id AS item_id,
    i.name AS item_name,
    i.description AS item_desc,
    cp.price,
    i.unit,
    i.is_big_price AS isBigPrice,
    i.is_salary AS isSalary
FROM categories c
JOIN items i ON c.category_key = i.category_key
JOIN city_prices cp ON i.id = cp.item_id
WHERE cp.city_key = 'beijing'
ORDER BY c.sort_order, i.sort_order;

-- ============================================
-- API 3: GET /api/categories/{categoryKey}/comparison
-- 获取某分类下所有城市的价格对比
-- 示例: categoryKey = 'dining'
-- ============================================
SELECT 
    i.sort_order - 1 AS `index`,
    i.name,
    GROUP_CONCAT(
        CONCAT('"', cp.city_key, '":', cp.price)
        ORDER BY cp.city_key
    ) AS prices_json,
    MIN(cp.price) AS min,
    MAX(cp.price) AS max
FROM items i
JOIN city_prices cp ON i.id = cp.item_id
WHERE i.category_key = 'dining'
GROUP BY i.id, i.name, i.sort_order
ORDER BY i.sort_order;

-- 更完整的查询（返回每个城市的价格）
SELECT 
    i.sort_order - 1 AS `index`,
    i.name,
    MAX(CASE WHEN cp.city_key = 'beijing' THEN cp.price END) AS beijing,
    MAX(CASE WHEN cp.city_key = 'shanghai' THEN cp.price END) AS shanghai,
    MAX(CASE WHEN cp.city_key = 'shenzhen' THEN cp.price END) AS shenzhen,
    MAX(CASE WHEN cp.city_key = 'guangzhou' THEN cp.price END) AS guangzhou,
    MIN(cp.price) AS min,
    MAX(cp.price) AS max
FROM items i
JOIN city_prices cp ON i.id = cp.item_id
WHERE i.category_key = 'dining'
GROUP BY i.id, i.name, i.sort_order
ORDER BY i.sort_order;

-- ============================================
-- API 4: GET /api/compare?cities=beijing,shanghai
-- 多城市对比
-- ============================================

-- 获取月度预估对比
SELECT 
    city_key,
    single_estimate AS single
FROM monthly_estimates
WHERE city_key IN ('beijing', 'shanghai');

-- 获取平均薪资对比
SELECT 
    cp.city_key,
    cp.price AS avgSalary
FROM city_prices cp
JOIN items i ON cp.item_id = i.id
WHERE i.is_salary = TRUE
AND cp.city_key IN ('beijing', 'shanghai');

-- 获取市中心定义对比
SELECT 
    city_key,
    center_def AS centerDef
FROM cities
WHERE city_key IN ('beijing', 'shanghai');

-- 获取分类价格对比
SELECT 
    c.category_key,
    cp.city_key,
    i.name,
    cp.price,
    i.unit
FROM categories c
JOIN items i ON c.category_key = i.category_key
JOIN city_prices cp ON i.id = cp.item_id
WHERE cp.city_key IN ('beijing', 'shanghai')
ORDER BY c.sort_order, i.sort_order, cp.city_key;

-- ============================================
-- API 5: GET /api/cities/{cityKey}/estimate
-- 获取城市月度预估支出
-- 示例: cityKey = 'beijing'
-- ============================================
SELECT 
    me.city_key AS cityKey,
    c.name AS cityName,
    me.single_estimate AS single
FROM monthly_estimates me
JOIN cities c ON me.city_key = c.city_key
WHERE me.city_key = 'beijing';

-- ============================================
-- 常用统计查询
-- ============================================

-- 各城市生活成本排名（基于月度预估）
SELECT 
    c.name AS city_name,
    me.single_estimate,
    RANK() OVER (ORDER BY me.single_estimate DESC) AS cost_rank
FROM monthly_estimates me
JOIN cities c ON me.city_key = c.city_key;

-- 各分类平均价格对比
SELECT 
    cat.name AS category_name,
    c.name AS city_name,
    ROUND(AVG(cp.price), 2) AS avg_price
FROM city_prices cp
JOIN items i ON cp.item_id = i.id
JOIN categories cat ON i.category_key = cat.category_key
JOIN cities c ON cp.city_key = c.city_key
WHERE i.is_big_price = FALSE
GROUP BY cat.category_key, cat.name, c.city_key, c.name
ORDER BY cat.sort_order, avg_price DESC;

-- 价格差异最大的项目
SELECT 
    i.name AS item_name,
    cat.name AS category_name,
    MIN(cp.price) AS min_price,
    MAX(cp.price) AS max_price,
    MAX(cp.price) - MIN(cp.price) AS price_diff,
    ROUND((MAX(cp.price) - MIN(cp.price)) / MIN(cp.price) * 100, 2) AS diff_percent
FROM city_prices cp
JOIN items i ON cp.item_id = i.id
JOIN categories cat ON i.category_key = cat.category_key
WHERE i.is_big_price = FALSE
GROUP BY i.id, i.name, cat.name
ORDER BY diff_percent DESC
LIMIT 10;
