from typing import List
from datetime import date
from app.models.core import CoreModel


class BurndownChartDataPoint(CoreModel):
    t: date
    y: int


class BurndownChartDataset(CoreModel):
    added: List[BurndownChartDataPoint]
    burned: List[BurndownChartDataPoint]
    current: List[BurndownChartDataPoint]