from django.urls import path

from .views import FeedbackListApi, FeedbackUpdateAPI

urlpatterns = [
    path('api/v1/updateFeedbacks/<int:pk>', FeedbackUpdateAPI.as_view(), name='feedback_update'),
    path('api/v1/allFeedbacks', FeedbackListApi.as_view(), name='feedback_list'),
]