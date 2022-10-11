from rest_framework import serializers
from users.models import User
from organizers.models import Organizer, Workspace
from voters.models import Voter
from polls.models import Poll, Candidate
from ballot.models import Ballot

class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User

        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password'
        ]

        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def create(self, validated_data):

        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

class OrganizerSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source='user.username')

    class Meta:

        model  = Organizer

        fields = [
            'user',
            'image',
            'phone',
            'country',
            'paid_status',
            'running_package'
        ]

class WorkspaceSerializer(serializers.ModelSerializer):

    class Meta:

        model = Workspace

        fields = [
            'name',
            'organizer',
            'voter_limit',
            'poll_limit'
        ]

class VoterSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source='user.username')

    class Meta:

        model = Voter

        fields = [
            'user',
            'country',
            'workspace'
        ]

class PollSerializer(serializers.ModelSerializer):

    class Meta:

        model = Poll

        fields = [
            'seat',
            'intro',
            'open',
            'begin_date',
            'end_date',
            'organizer',
            'workspace'
        ]

class CandidateSerializer(serializers.ModelSerializer):

    class Meta:

        model = Candidate

        fields = [
            'organizer',
            'poll',
            'first_name',
            'last_name',
            'email',
            'image',
            'country',
            'bio'
        ]

class BallotSerializer(serializers.ModelSerializer):

    class Meta:

        model = Ballot

        fields = [
            'voter',
            'poll',
            'candidate',
        ]