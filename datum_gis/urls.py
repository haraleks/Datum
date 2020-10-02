from django.urls import path
from datum_gis.views import (PointView, LineView, LoadData, MinLenght, MinScore)


as_view_common = {
    'get': 'list',
}

as_view_with_pk = {
    'get': 'retrieve',
    'delete': 'destroy'
}

urlpatterns = [
    path('point/', PointView.as_view(as_view_common), name='point'),
    path('point/<int:pk>/', PointView.as_view(as_view_with_pk), name='point_pk'),
    path('line/', LineView.as_view(as_view_common), name='line'),
    path('line/<int:pk>/', LineView.as_view(as_view_with_pk), name='line_pk'),
    path('load_data/', LoadData.as_view({'get': 'get_public_api'}), name='load_data'),
    path('min_length/', MinLenght.as_view({'get': 'get_min_lenght'}), name='min_length'),
    path('min_score/', MinScore.as_view({'get': 'get_min_score'}), name='min_score'),

]
