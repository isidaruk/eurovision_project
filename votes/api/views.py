from django.http import Http404
from django.core.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from votes.models import Vote
from votes.api.serializers import VoteSerializer
from votes.api.services import check_voters, check_token

import logging


logger = logging.getLogger('vote')


# class VoteList(APIView):
class VoteList(GenericAPIView):
    """
    List all votes, or create a new vote.
    """

    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    def get(self, request, format=None):
        # print(request)
        votes = Vote.objects.all()
        serializer = VoteSerializer(votes, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):

        logger.info('Test log.')

        # Token validation
        # sended_vote_key = request.headers.get('Token')

        if not check_token(request.headers.get('Token'), request.data.get('from_voter')):
            raise PermissionDenied()

        serializer = VoteSerializer(data=request.data, context={'request': request})
        # print(request.headers.get('Token'))

        if serializer.is_valid():
            # Custom Token validation.

            errors = check_voters(serializer.validated_data)

            if errors:
                return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Vote was accepted.
                serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VoteDetail(APIView):
    """
    Retrieve, update or delete a vote instance.
    """

    def get_object(self, pk):
        try:
            return Vote.objects.get(pk=pk)
        except Vote.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        vote = self.get_object(pk)
        serializer = VoteSerializer(vote, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        vote = self.get_object(pk)
        serializer = VoteSerializer(vote, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        vote = self.get_object(pk)
        vote.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
