from rest_framework import permissions, viewsets

from permissions import IsOwnerOrReadOnly
from talk.models import Talk
from talk.serializers import TalkSerializer


class TalkViewSet(viewsets.ModelViewSet):
    serializer_class = TalkSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = Talk.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# TODO: Этот проект Survival Guide интегрировать в проект Todolist и после этого проект Survival Guide удалить из Heroku
# TODO: Add paging for HTML views & DRF API
# TODO: Write tests for the API calls
