# 城市生活成本查询 API 文档

## 概述

本文档定义了城市生活成本查询应用所需的后端 API 接口，用于支持前后端分离架构。

**Base URL:** `/api`

---

## 接口列表

| 接口 | 方法 | 用途 |
|------|------|------|
| `/api/cities` | GET | 获取支持的城市列表 |
| `/api/cities/{cityKey}/costs` | GET | 获取指定城市的完整生活成本数据 |
| `/api/categories/{categoryKey}/comparison` | GET | 获取某分类下所有城市的价格对比 |
| `/api/compare` | GET | 多城市对比 |
| `/api/cities/{cityKey}/estimate` | GET | 获取城市月度预估支出 |

---

## 1. 获取城市列表

### 请求

```
GET /api/cities
```

### 响应

```json
{
  "cities": [
    {
      "key": "beijing",
      "name": "北京",
      "emoji": "🏛️",
      "centerDef": "三环内"
    },
    {
      "key": "shanghai",
      "name": "上海",
      "emoji": "🌆",
      "centerDef": "内环内"
    },
    {
      "key": "shenzhen",
      "name": "深圳",
      "emoji": "🏙️",
      "centerDef": "福田/南山核心区"
    },
    {
      "key": "guangzhou",
      "name": "广州",
      "emoji": "🌺",
      "centerDef": "天河/越秀核心区"
    }
  ]
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `key` | string | 城市唯一标识 |
| `name` | string | 城市中文名称 |
| `emoji` | string | 城市图标 |
| `centerDef` | string | 市中心定义 |

---

## 2. 获取城市生活成本详情

### 请求

```
GET /api/cities/{cityKey}/costs
```

### 路径参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `cityKey` | string | 是 | 城市标识 (beijing / shanghai / shenzhen / guangzhou) |

### 响应

```json
{
  "city": {
    "key": "beijing",
    "name": "北京",
    "centerDef": "三环内",
    "emoji": "🏛️"
  },
  "monthlyEstimate": {
    "single": 8500
  },
  "categories": {
    "dining": {
      "name": "餐饮",
      "icon": "🥗",
      "items": [
        {
          "name": "平价餐厅一顿饭",
          "desc": "普通快餐/盖浇饭/工作餐",
          "price": 40,
          "unit": "元"
        },
        {
          "name": "中档餐厅两人餐",
          "desc": "三道菜，如海底捞等",
          "price": 320,
          "unit": "元"
        },
        {
          "name": "麦当劳套餐",
          "desc": "标准化价格参考",
          "price": 42,
          "unit": "元"
        },
        {
          "name": "咖啡（常规）",
          "desc": "星巴克/瑞幸",
          "price": 30,
          "unit": "元"
        },
        {
          "name": "饮料 (330ml)",
          "desc": "",
          "price": 6,
          "unit": "元"
        },
        {
          "name": "瓶装水 (330ml)",
          "desc": "",
          "price": 2.5,
          "unit": "元"
        }
      ]
    },
    "market": {
      "name": "超市/市场",
      "icon": "🛒",
      "items": [...]
    },
    "transport": {
      "name": "交通",
      "icon": "🚗",
      "items": [...]
    },
    "utilities": {
      "name": "生活杂费",
      "icon": "⚡",
      "items": [...]
    },
    "leisure": {
      "name": "运动与休闲",
      "icon": "🏸",
      "items": [...]
    },
    "clothing": {
      "name": "服装",
      "icon": "👕",
      "items": [...]
    },
    "housing": {
      "name": "租房",
      "icon": "🏠",
      "items": [...]
    },
    "salary": {
      "name": "薪资与购房",
      "icon": "💰",
      "items": [...]
    }
  }
}
```

### Item 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | 是 | 项目名称 |
| `desc` | string | 否 | 项目描述 |
| `price` | number | 是 | 价格 |
| `unit` | string | 是 | 单位（元、元/月等） |
| `isBigPrice` | boolean | 否 | 是否为大额价格（如购车、房价），默认 false |
| `isSalary` | boolean | 否 | 是否为薪资数据，默认 false |

---

## 3. 获取分类价格对比

用于显示价格范围条，展示当前价格在所有城市中的位置。

### 请求

```
GET /api/categories/{categoryKey}/comparison
```

### 路径参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `categoryKey` | string | 是 | 分类标识 |

### 分类标识列表

| categoryKey | 名称 |
|-------------|------|
| `dining` | 餐饮 |
| `market` | 超市/市场 |
| `transport` | 交通 |
| `utilities` | 生活杂费 |
| `leisure` | 运动与休闲 |
| `clothing` | 服装 |
| `housing` | 租房 |
| `salary` | 薪资与购房 |

### 响应

```json
{
  "category": "dining",
  "categoryName": "餐饮",
  "items": [
    {
      "index": 0,
      "name": "平价餐厅一顿饭",
      "prices": {
        "beijing": 40,
        "shanghai": 38,
        "shenzhen": 35,
        "guangzhou": 30
      },
      "min": 30,
      "max": 40
    },
    {
      "index": 1,
      "name": "中档餐厅两人餐",
      "prices": {
        "beijing": 320,
        "shanghai": 300,
        "shenzhen": 280,
        "guangzhou": 250
      },
      "min": 250,
      "max": 320
    }
  ]
}
```

---

## 4. 多城市对比

### 请求

```
GET /api/compare?cities=beijing,shanghai
```

### 查询参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `cities` | string | 是 | 逗号分隔的城市标识列表，至少2个 |

### 响应

```json
{
  "cities": ["beijing", "shanghai"],
  "comparison": {
    "monthlyEstimate": {
      "beijing": {
        "single": 8500
      },
      "shanghai": {
        "single": 8200
      }
    },
    "avgSalary": {
      "beijing": 12500,
      "shanghai": 12800
    },
    "centerDef": {
      "beijing": "三环内",
      "shanghai": "内环内"
    },
    "categories": {
      "dining": {
        "beijing": [
          { "name": "平价餐厅一顿饭", "price": 40, "unit": "元" }
        ],
        "shanghai": [
          { "name": "平价餐厅一顿饭", "price": 38, "unit": "元" }
        ]
      }
    }
  }
}
```

---

## 5. 获取城市月度预估支出

### 请求

```
GET /api/cities/{cityKey}/estimate
```

### 路径参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `cityKey` | string | 是 | 城市标识 |

### 响应

```json
{
  "cityKey": "beijing",
  "cityName": "北京",
  "estimate": {
    "single": 8500
  }
}
```

---

## 错误响应

### 格式

```json
{
  "error": {
    "code": "CITY_NOT_FOUND",
    "message": "城市不存在"
  }
}
```

### 错误码列表

| HTTP 状态码 | 错误码 | 说明 |
|-------------|--------|------|
| 400 | `INVALID_PARAMS` | 请求参数无效 |
| 404 | `CITY_NOT_FOUND` | 城市不存在 |
| 404 | `CATEGORY_NOT_FOUND` | 分类不存在 |
| 500 | `INTERNAL_ERROR` | 服务器内部错误 |

---

## 数据模型

### City（城市）

| 字段 | 类型 | 说明 |
|------|------|------|
| `key` | string | 城市唯一标识 |
| `name` | string | 城市中文名称 |
| `emoji` | string | 城市图标 |
| `centerDef` | string | 市中心定义 |

### Category（分类）

| 字段 | 类型 | 说明 |
|------|------|------|
| `name` | string | 分类名称 |
| `icon` | string | 分类图标 |
| `items` | Item[] | 价格项目列表 |

### Item（价格项目）

| 字段 | 类型 | 说明 |
|------|------|------|
| `name` | string | 项目名称 |
| `desc` | string | 项目描述（可选） |
| `price` | number | 价格 |
| `unit` | string | 单位 |
| `isBigPrice` | boolean | 是否为大额价格 |
| `isSalary` | boolean | 是否为薪资数据 |

### MonthlyEstimate（月度预估）

| 字段 | 类型 | 说明 |
|------|------|------|
| `single` | number | 单人预估月支出 |

---

## 附录：完整分类数据结构

### 餐饮 (dining)

| 项目 | 描述 | 单位 |
|------|------|------|
| 平价餐厅一顿饭 | 普通快餐/盖浇饭/工作餐 | 元 |
| 中档餐厅两人餐 | 三道菜，如海底捞等 | 元 |
| 麦当劳套餐 | 标准化价格参考 | 元 |
| 咖啡（常规） | 星巴克/瑞幸 | 元 |
| 饮料 (330ml) | - | 元 |
| 瓶装水 (330ml) | - | 元 |

### 超市/市场 (market)

| 项目 | 描述 | 单位 |
|------|------|------|
| 牛奶 (1L) | - | 元 |
| 大米 (1kg) | - | 元 |
| 鸡蛋 (12个) | - | 元 |
| 猪肉 (1kg) | - | 元 |
| 鸡胸肉 (1kg) | - | 元 |
| 牛肉 (1kg) | 牛腿肉/适合炒菜 | 元 |
| 苹果 (1kg) | - | 元 |
| 香蕉 (1kg) | - | 元 |
| 橙子 (1kg) | - | 元 |
| 番茄 (1kg) | - | 元 |
| 土豆 (1kg) | - | 元 |
| 洋葱 (1kg) | - | 元 |
| 青菜/绿叶菜 (1kg) | - | 元 |
| 瓶装水 (1.5L) | - | 元 |

### 交通 (transport)

| 项目 | 描述 | 单位 |
|------|------|------|
| 单程车票（公交/地铁） | - | 元 |
| 出租车起步价 | 含网约车参考 | 元 |
| 出租车 1km 计费 | - | 元 |
| 出租车等候 (1小时) | - | 元 |
| 汽油 (1L) | - | 元 |
| 购车（大众Golf） | 中型燃油车参考 | 元 |
| 购车（特斯拉Model 3） | 电车参考 | 元 |

### 生活杂费 (utilities)

| 项目 | 描述 | 单位 |
|------|------|------|
| 基础水电煤 (85平米) | 电费+水费+燃气+物业 | 元/月 |
| 手机套餐 (30GB+) | 三大运营商5G套餐 | 元/月 |
| 宽带 (300Mbps+) | - | 元/月 |

### 运动与休闲 (leisure)

| 项目 | 描述 | 单位 |
|------|------|------|
| 健身房月卡 | - | 元/月 |
| 羽毛球场 (1小时/周末) | - | 元 |
| 电影票 | - | 元 |

### 服装 (clothing)

| 项目 | 描述 | 单位 |
|------|------|------|
| 牛仔裤 | - | 元 |
| 上衣 (Zara/H&M/优衣库) | - | 元 |
| 运动鞋 (安踏/耐克) | - | 元 |

### 租房 (housing)

| 项目 | 描述 | 单位 |
|------|------|------|
| 市中心一居室 | 根据城市定义 | 元/月 |
| 非市中心一居室 | 根据城市定义 | 元/月 |
| 市中心三居室 | 根据城市定义 | 元/月 |
| 非市中心三居室 | 根据城市定义 | 元/月 |

### 薪资与购房 (salary)

| 项目 | 描述 | 单位 |
|------|------|------|
| 市中心房价 (每平米) | 根据城市定义 | 元 |
| 非市中心房价 (每平米) | 根据城市定义 | 元 |
| 税后平均月薪 | - | 元 |
