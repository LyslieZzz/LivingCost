from pydantic import BaseModel, Field


class ItemResponse(BaseModel):
    name: str = Field(..., description="项目名称")
    desc: str = Field("", description="项目描述")
    price: float = Field(..., description="价格")
    unit: str = Field(..., description="单位")
    isBigPrice: bool = Field(False, description="是否为大额价格")
    isSalary: bool = Field(False, description="是否为薪资数据")

    model_config = {"from_attributes": True}


class CategoryResponse(BaseModel):
    name: str = Field(..., description="分类名称")
    icon: str = Field(..., description="分类图标")
    items: list[ItemResponse] = Field(..., description="价格项目列表")


class MonthlyEstimateResponse(BaseModel):
    single: float = Field(..., description="单人预估月支出")


class CityInfoResponse(BaseModel):
    key: str = Field(..., description="城市唯一标识")
    name: str = Field(..., description="城市中文名称")
    centerDef: str = Field(..., description="市中心定义")
    emoji: str = Field(..., description="城市图标")


class CostResponse(BaseModel):
    city: CityInfoResponse = Field(..., description="城市信息")
    monthlyEstimate: MonthlyEstimateResponse = Field(..., description="月度预估")
    categories: dict[str, CategoryResponse] = Field(..., description="各分类数据")


class EstimateResponse(BaseModel):
    cityKey: str = Field(..., description="城市标识")
    cityName: str = Field(..., description="城市名称")
    estimate: MonthlyEstimateResponse = Field(..., description="月度预估")
