# from rest_framework import viewsets

# from votes.models import Vote
# from votes.api.serializers import VoteSerializer


# class VoteViewSet(viewsets.ModelViewSet):
#     queryset = Vote.objects.all()
#     serializer_class = VoteSerializer


from votes.models import Vote
from votes.api.serializers import VoteSerializer
from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

# Should be moved to the top.
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from votes.models import Vote
from voters.models import Voter
from participants.models import Participant


# class VoteList(APIView):
class VoteList(GenericAPIView):
    """
    List all votes, or create a new vote.
    """

    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    def get(self, request, format=None):
        print(request)
        votes = Vote.objects.all()
        serializer = VoteSerializer(votes, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = VoteSerializer(data=request.data, context={'request': request})
        # print(request.headers.get('Token'))

        if serializer.is_valid():
            # Custom Token validation.
            sended_vote_key = request.headers.get('Token')

            from_voter = serializer.validated_data.get('from_voter')

            # -*- Check Cases -*-

            to_participant = serializer.validated_data.get('to_participant')

            vote_point = serializer.validated_data.get('point')

            # print(from_voter, type(from_voter))
            # print(to_participant, type(to_participant))

            voter = Voter.objects.get(id=from_voter.id)
            participant = Participant.objects.get(id=to_participant.id)

            # If voter have Token.
            if from_voter and sended_vote_key:
                if str(from_voter.vote_key) != str(sended_vote_key):
                    return HttpResponseForbidden(content='You are not allowed to vote this year.')

                # Count how many times voter has voted.
                if Vote.objects.filter(from_voter=from_voter.id).count() == 10:
                    return HttpResponseBadRequest(content="You've voted 10 times.")

                # If the point is not used.
                if Vote.objects.filter(from_voter=from_voter.id).filter(point__iexact=vote_point).count() != 0:  # ?
                    return HttpResponseBadRequest(content=f"{vote_point} point is already given.")

                # Voting for your own country.
                if voter.country.name == participant.country.name:
                    return HttpResponseBadRequest(content='You are not allowed to vote for your own country.')

                # Check vote for the same country.
                if not Vote.objects.filter(to_participant=to_participant.id).exists():
                    print('Your vote was accepted.')
                    serializer.save()
                else:
                    return HttpResponseBadRequest(content="You've already given a point to these participant.")

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
