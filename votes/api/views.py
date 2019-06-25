import logging

from django.core.exceptions import PermissionDenied
from django.http import Http404

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from voters.models import Voter
from votes.api.serializers import VoteSerializer
from votes.api.services import check_token, check_voters
from votes.models import Vote

logger = logging.getLogger('vote')


class VoteList(GenericAPIView):
    """
    List all votes, or create a new vote.
    """

    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    def get(self, request, format=None):
        votes = Vote.objects.all()
        serializer = VoteSerializer(votes, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        from_voter = request.data.get('from_voter')

        # Token validation.
        if not check_token(request.headers.get('Token'), from_voter):
            logger.error(f"Token provided isn't valid. Voter id is: {from_voter}")
            raise PermissionDenied()

        serializer = VoteSerializer(data=request.data)

        if serializer.is_valid():
            errors, data = check_voters(serializer.validated_data)

            if errors:
                logger.warning(f'Voter {data[1]} failed to vote for {data[2]} with {data[0]} points: {errors}')
                return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Vote was accepted.
                logger.info(f'Voter {data[1]} gave {data[0]} points to {data[2]}')
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            logger.error(f'Data is not valid: {serializer.errors}')
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
