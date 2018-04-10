from rest_framework import viewsets
from rest_framework import permissions
from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from tracks.permissions import IsOwnerOrReadOnly

from .serializers import PlayListSerializer
from django.contrib.auth import get_user_model
from rest_framework.decorators import permission_classes

from .models import PlayList

# Create your views here.
def test_view(request):
	return render(request, 'test.html')

class PlayListViewSet(viewsets.ModelViewSet):
	serializer_class = PlayListSerializer
	permission_classes = (permissions.IsAuthenticated,)

	def get(self, request, *args, **kwargs):
		User = get_user_model()
		self.object = get_object_or_404(User, pk=request.user.id)
		serializer = self.get_serializer(self.object)
		return Response(serializer.data)

	def get_queryset(self):
		return PlayList.objects.filter(user=self.request.user)