from rest_framework import mixins
from rest_framework.generics import GenericAPIView

from .models import Feedbacks
from .seriallizers import FeedbackSerializer
from .urils.decorators import token_valid


class FeedbackUpdateAPI(mixins.UpdateModelMixin,
                        GenericAPIView):
    """Update feedback by pk"""
    queryset = Feedbacks.objects.all()
    serializer_class = FeedbackSerializer

    @token_valid
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class FeedbackListApi(mixins.ListModelMixin,
                      GenericAPIView):
    """Get all feedbacks"""
    queryset = Feedbacks.objects.all()
    serializer_class = FeedbackSerializer
    
    @token_valid
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)