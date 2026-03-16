-- ============================================
-- 城市生活成本查询系统 - 数据库表结构
-- Database: MySQL 8.0+
-- ============================================

-- 设置字符集
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- ============================================
-- 1. 城市表 (cities)
-- 存储城市基本信息
-- ============================================
CREATE TABLE IF NOT EXISTS cities (
    city_key VARCHAR(50) PRIMARY KEY COMMENT '城市唯一标识 (beijing, shanghai 等)',
    name VARCHAR(100) NOT NULL COMMENT '城市中文名称',
    emoji VARCHAR(10) NOT NULL COMMENT '城市图标',
    center_def VARCHAR(200) NOT NULL COMMENT '市中心定义描述',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='城市信息表';

-- ============================================
-- 2. 分类表 (categories)
-- 存储消费分类信息
-- ============================================
CREATE TABLE IF NOT EXISTS categories (
    category_key VARCHAR(50) PRIMARY KEY COMMENT '分类唯一标识 (dining, market 等)',
    name VARCHAR(100) NOT NULL COMMENT '分类中文名称',
    icon VARCHAR(10) NOT NULL COMMENT '分类图标',
    sort_order INT DEFAULT 0 COMMENT '排序顺序'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='消费分类表';

-- ============================================
-- 3. 价格项目表 (items)
-- 存储具体消费项目的元数据
-- ============================================
CREATE TABLE IF NOT EXISTS items (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '项目ID',
    category_key VARCHAR(50) NOT NULL COMMENT '所属分类',
    name VARCHAR(200) NOT NULL COMMENT '项目名称',
    description VARCHAR(500) DEFAULT '' COMMENT '项目描述',
    unit VARCHAR(50) NOT NULL COMMENT '单位（元、元/月等）',
    is_big_price BOOLEAN DEFAULT FALSE COMMENT '是否为大额价格（如购车、房价）',
    is_salary BOOLEAN DEFAULT FALSE COMMENT '是否为薪资数据',
    sort_order INT DEFAULT 0 COMMENT '在分类内的排序顺序',
    CONSTRAINT fk_items_category FOREIGN KEY (category_key) REFERENCES categories(category_key) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='价格项目表';

-- ============================================
-- 4. 城市价格表 (city_prices)
-- 存储各城市的具体价格数据（核心关联表）
-- ============================================
CREATE TABLE IF NOT EXISTS city_prices (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '记录ID',
    city_key VARCHAR(50) NOT NULL COMMENT '城市标识',
    item_id INT NOT NULL COMMENT '项目ID',
    price DECIMAL(12,2) NOT NULL COMMENT '价格',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '价格更新时间',
    CONSTRAINT fk_city_prices_city FOREIGN KEY (city_key) REFERENCES cities(city_key) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_city_prices_item FOREIGN KEY (item_id) REFERENCES items(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT uk_city_item UNIQUE (city_key, item_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='城市价格表';

-- ============================================
-- 5. 月度预估表 (monthly_estimates)
-- 存储各城市的月度支出预估
-- ============================================
CREATE TABLE IF NOT EXISTS monthly_estimates (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '记录ID',
    city_key VARCHAR(50) NOT NULL UNIQUE COMMENT '城市标识',
    single_estimate DECIMAL(10,2) NOT NULL COMMENT '单人月度预估支出',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    CONSTRAINT fk_monthly_estimates_city FOREIGN KEY (city_key) REFERENCES cities(city_key) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='月度预估表';

-- ============================================
-- 索引优化
-- ============================================

-- items 表索引
CREATE INDEX idx_items_category ON items(category_key);
CREATE INDEX idx_items_sort ON items(category_key, sort_order);

-- city_prices 表索引
CREATE INDEX idx_city_prices_city ON city_prices(city_key);
CREATE INDEX idx_city_prices_item ON city_prices(item_id);
CREATE INDEX idx_city_prices_updated ON city_prices(updated_at);

-- monthly_estimates 表索引
CREATE INDEX idx_monthly_estimates_updated ON monthly_estimates(updated_at);
