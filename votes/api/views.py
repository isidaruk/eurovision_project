# from rest_framework import viewsets

# from votes.models import Vote
# from votes.api.serializers import VoteSerializer


# class VoteViewSet(viewsets.ModelViewSet):
#     queryset = Vote.objects.all()
#     serializer_class = VoteSerializer


from votes.models import Vote
from votes.api.serializers import VoteSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status


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
            print('X-auth-token:', sended_vote_key)

            from_voter = serializer.validated_data.get('from_voter')
            print('Vote Key', from_voter.vote_key)

            if from_voter and sended_vote_key:
                if str(from_voter.vote_key) == str(sended_vote_key):
                    print('Your vote was accepted.')
                elif from_voter.vote_key != sended_vote_key:
                    # from django.http import HttpResponseBadRequest
                    # return HttpResponseBadRequest(content='You are not allowed to vote.')

                    from django.core.exceptions import PermissionDenied
                    raise PermissionDenied()

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
