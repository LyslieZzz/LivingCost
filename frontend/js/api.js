/**
 * API 模块 - 生活成本查询网站
 * 后端运行在 http://localhost:8000
 */

const API_BASE_URL = 'http://localhost:8000/api';

// 缓存对象
let cities = null;         // 城市列表缓存
const cityData = {};       // 各城市数据缓存 { beijing: {...}, shanghai: {...} }
const priceRanges = {};    // 价格范围缓存 { categoryKey: { itemIndex: { min, max } } }

/**
 * 统一处理响应，非 ok 时抛出错误
 * @param {Response} response - fetch 返回的 Response 对象
 * @returns {Promise<Object>} 解析后的 JSON 数据
 */
async function handleResponse(response) {
  if (!response.ok) {
    const text = await response.text();
    let message = `HTTP ${response.status}: ${response.statusText}`;
    try {
      const json = JSON.parse(text);
      if (json.detail) message = typeof json.detail === 'string' ? json.detail : JSON.stringify(json.detail);
    } catch (_) {
      if (text) message = text;
    }
    throw new Error(message);
  }
  return response.json();
}

/**
 * 获取城市列表，有缓存直接返回
 * @returns {Promise<Array>} 城市列表
 */
async function fetchCities() {
  if (cities !== null) return cities;
  const res = await fetch(`${API_BASE_URL}/cities`);
  const data = await handleResponse(res);
  cities = data.cities;
  return cities;
}

/**
 * 获取指定城市完整数据，有缓存直接返回
 * @param {string} cityKey - 城市 key，如 'beijing', 'shanghai'
 * @returns {Promise<Object>} 城市数据 { city, monthlyEstimate, categories }
 */
async function fetchCityCosts(cityKey) {
  if (cityData[cityKey]) return cityData[cityKey];
  const res = await fetch(`${API_BASE_URL}/cities/${cityKey}/costs`);
  const data = await handleResponse(res);
  cityData[cityKey] = data;
  return data;
}

/**
 * 获取所有城市数据（用于初始化）
 * @returns {Promise<Object>} 所有城市数据，结构与 CITY_DATA 兼容
 */
async function fetchAllCitiesData() {
  const cityList = await fetchCities();
  const keys = cityList.map(c => (typeof c === 'string' ? c : c.key));
  const results = await Promise.all(keys.map(key => fetchCityCosts(key)));
  const out = {};
  keys.forEach((key, i) => {
    out[key] = results[i];
  });
  return out;
}

/**
 * 获取跨城市价格对比
 * @param {string} categoryKey - 分类 key，如 'dining', 'market'
 * @returns {Promise<Object>} { category, categoryName, items: [{ index, name, prices, min, max }] }
 */
async function fetchCategoryComparison(categoryKey) {
  const res = await fetch(`${API_BASE_URL}/categories/${categoryKey}/comparison`);
  const data = await handleResponse(res);
  if (!priceRanges[categoryKey]) priceRanges[categoryKey] = {};
  data.items.forEach(item => {
    priceRanges[categoryKey][item.index] = { min: item.min, max: item.max };
  });
  return data;
}

/**
 * 获取缓存的城市数据
 * @param {string} cityKey - 城市 key
 * @returns {Object|undefined} 缓存的城市数据，无则返回 undefined
 */
function getCachedCityData(cityKey) {
  return cityData[cityKey];
}

/**
 * 获取缓存的价格范围
 * @param {string} categoryKey - 分类 key
 * @param {number} itemIndex - 项目索引
 * @returns {Object|undefined} { min, max }，无则返回 undefined
 */
function getCachedPriceRange(categoryKey, itemIndex) {
  const cat = priceRanges[categoryKey];
  return cat ? cat[itemIndex] : undefined;
}

/**
 * 清除所有缓存
 */
function clearCache() {
  cities = null;
  Object.keys(cityData).forEach(k => delete cityData[k]);
  Object.keys(priceRanges).forEach(k => delete priceRanges[k]);
}

// 挂载到 window.API
window.API = {
  API_BASE_URL,
  handleResponse,
  fetchCities,
  fetchCityCosts,
  fetchAllCitiesData,
  fetchCategoryComparison,
  getCachedCityData,
  getCachedPriceRange,
  clearCache,
};
