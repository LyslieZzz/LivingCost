from pydantic import BaseModel, Field


class CategoryComparisonItem(BaseModel):
    index: int = Field(..., description="项目索引")
    name: str = Field(..., description="项目名称")
    prices: dict[str, float] = Field(..., description="各城市价格")
    min: float = Field(..., description="最低价格")
    max: float = Field(..., description="最高价格")


class CategoryComparisonResponse(BaseModel):
    category: str = Field(..., description="分类标识")
    categoryName: str = Field(..., description="分类名称")
    items: list[CategoryComparisonItem] = Field(..., description="项目对比列表")


class CompareItemResponse(BaseModel):
    name: str = Field(..., description="项目名称")
    price: float = Field(..., description="价格")
    unit: str = Field(..., description="单位")


class MonthlyEstimateCompare(BaseModel):
    single: float = Field(..., description="单人预估月支出")


class CompareResponse(BaseModel):
    cities: list[str] = Field(..., description="对比的城市列表")
    comparison: dict = Field(..., description="对比数据")
