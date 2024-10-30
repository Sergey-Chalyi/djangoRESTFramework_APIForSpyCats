"""
URL configuration for base project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.urls import path

from agency.views import SpyCatListView, SpyCatDetailView, MissionListView, MissionDetailView, MissionAssignCatView, \
    MissionCompleteView, TargetUpdateView, TargetCompleteView

urlpatterns = [
    path('api/v1/cats/', SpyCatListView.as_view(), name='spycat-list'),
    path('api/v1/cats/<int:pk>/', SpyCatDetailView.as_view(), name='spycat-detail'),

    path('api/v1/missions/', MissionListView.as_view(), name='mission-list'),
    path('api/v1/missions/<int:pk>/', MissionDetailView.as_view(), name='mission-detail'),
    path('api/v1/missions/<int:pk>/assign_cat/', MissionAssignCatView.as_view(), name='mission-assign-cat'),
    path('api/v1/missions/<int:pk>/complete/', MissionCompleteView.as_view(), name='mission-complete'),

    path('api/v1/targets/<int:pk>/', TargetUpdateView.as_view(), name='target-update'),
    path('api/v1/targets/<int:pk>/complete/', TargetCompleteView.as_view(), name='target-complete'),
]


