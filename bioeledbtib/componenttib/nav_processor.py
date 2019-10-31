# -*- coding: utf-8 -*-
#上下文渲染器 （context processor)
#好像没用上
from .models import Column
nav_display_columns = Column.objects.filter(nav_display=True)
def nav_column(request):
    return {'nav_display_columns': nav_display_columns}
