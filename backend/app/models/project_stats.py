from typing import Optional, Union, List
from app.models.core import CoreModel
from app.models.burndown_chart_datasets import BurndownChartDataset

class ProjectStatsBase(CoreModel):
    backlog_count: Optional[int]
    todo_count: Optional[int]
    ongoing_count: Optional[int]
    done_count: Optional[int]

    backlog_points: Optional[int]
    todo_points: Optional[int]
    ongoing_points: Optional[int]
    done_points: Optional[int]

    chart_data: Optional[BurndownChartDataset]

class ProjectStats(ProjectStatsBase):
    pass
