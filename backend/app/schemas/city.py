from pydantic import BaseModel, Field


class CityBase(BaseModel):
    key: str = Field(..., description="城市唯一标识", examples=["beijing"])
    name: str = Field(..., description="城市中文名称", examples=["北京"])
    emoji: str = Field(..., description="城市图标", examples=["🏛️"])
    centerDef: str = Field(..., description="市中心定义", examples=["三环内"])

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }


class CityResponse(CityBase):
    pass


class CitiesResponse(BaseModel):
    cities: list[CityBase]
