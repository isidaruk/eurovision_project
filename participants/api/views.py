# from rest_framework import viewsets

# from participants.models import Participant
# from participants.api.serializers import ParticipantSerializer


# class ParticipantViewSet(viewsets.ModelViewSet):
#     queryset = Participant.objects.all()
#     serializer_class = ParticipantSerializer


from participants.models import Participant
from participants.api.serializers import ParticipantSerializer
from django.http import Http404
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.core.cache import cache

# from django.conf import settings
# from django.core.cache.backends.base import DEFAULT_TIMEOUT


# CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


# class ParticipantList(APIView):
class ParticipantList(GenericAPIView):
    """
    List all participants, or create a new participant.
    """

    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer

    def get(self, request, format=None):
        participants = Participant.objects.all()
        serializer = ParticipantSerializer(participants, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ParticipantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ParticipantDetail(APIView):
    """
    Retrieve, update or delete a participant instance.
    """

    def get_object(self, pk):
        try:
            return Participant.objects.get(pk=pk)
        except Participant.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        participant = self.get_object(pk)
        serializer = ParticipantSerializer(participant)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        participant = self.get_object(pk)
        serializer = ParticipantSerializer(participant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        participant = self.get_object(pk)
        participant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
