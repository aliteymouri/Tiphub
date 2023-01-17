from django.urls import path
from . import views

app_name = 'video'
urlpatterns = [
    path("Videos", views.VideoListView.as_view(), name='video_list'),
    path("video/<str:slug>/", views.VideoDetailView.as_view(), name='video_detail'),
    path("search/", views.SearchView.as_view(), name='search'),
    path("category/<str:slug>", views.CatDetailView.as_view(), name='category_detail'),
    path("remove/<int:pk>", views.RemoveCommentView.as_view(), name='remove_comment'),
    path("like/<str:slug>/<int:pk>", views.like, name='like'),
    path("favorite/<str:slug>/<int:pk>", views.favorite, name='favorite'),
    path("favorites", views.FavoriteView.as_view(), name='favorites'),

]
