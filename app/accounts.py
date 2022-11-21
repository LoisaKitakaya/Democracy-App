from polls.models import Poll
from voters.models import Voter

class AccountObject():

    def __init__(self, workspace, organizer) -> None:

        self.workspace = workspace

        self.organizer = organizer

        self.FREE = 'FREE_TIER'
        self.PRO = 'PRO_TIER'
        self.BUSINESS = 'BUSINESS_TIER'
        self.ENTERPRISE = 'ENTERPRISE_TIER'

        self.FREE_TIER = (
            {"name": self.FREE, "poll_limit": 2, "voter_limit": 10, "price": "Free"},
        )

        self.PRO_TIER = (
            {"tier_name": self.PRO, "poll_limit": 4, "voter_limit": 100, "price": "KES 15000"},
        )

        self.BUSINESS_TIER = (
            {"tier_name": self.BUSINESS, "poll_limit": 8, "voter_limit": 1000, "price": "KES 35000"},
        )

        self.ENTERPRISE_TIER = (
            {"tier_name": self.ENTERPRISE, "poll_limit": 16, "voter_limit": 10000, "price": "KES 65000"},
        )

    def __str__(self) -> str:
        
        return f'[{self.organizer.user.username}: {self.workspace.name}]'

    def check_tier(self):

        tier = self.organizer.running_package

        poll_limit = self.workspace.poll_limit
        voter_limit = self.workspace.voter_limit

        if tier == "FREE_TIER" and poll_limit == 2 and voter_limit == 10:

            account_tier = self.FREE_TIER

            return account_tier

        elif tier == "PRO_TIER" and poll_limit == 4 and voter_limit == 100:

            account_tier = self.PRO_TIER

            return account_tier

        elif tier == "BUSINESS_TIER" and poll_limit == 8 and voter_limit == 1000:

            account_tier = self.BUSINESS_TIER

            return account_tier

        elif tier == "ENTERPRISE_TIER" and poll_limit == 16 and voter_limit == 10000:

            account_tier = self.ENTERPRISE_TIER

            return account_tier

        else:

            return f'Something is not right'

    def upgrade_account(self, tier):

        if tier == "PRO_TIER":

            organizer = self.organizer
            workspace = self.workspace

            organizer.running_package = self.PRO
            organizer.paid_status = True
            organizer.save()

            workspace.poll_limit = self.PRO_TIER[0]["poll_limit"]
            workspace.voter_limit = self.PRO_TIER[0]["voter_limit"]
            workspace.save()

            message = "You have upgraded to Pollar PRO package."

            return message

        elif tier == "BUSINESS_TIER":

            organizer = self.organizer
            workspace = self.workspace

            organizer.running_package = self.BUSINESS
            organizer.paid_status = True
            organizer.save()

            workspace.poll_limit = self.BUSINESS_TIER[0]["poll_limit"]
            workspace.voter_limit = self.BUSINESS_TIER[0]["voter_limit"]
            workspace.save()

            message = "You have upgraded to Pollar BUSINESS package."

            return message

        elif tier == "ENTERPRISE_TIER":

            organizer = self.organizer
            workspace = self.workspace

            organizer.running_package = self.ENTERPRISE
            organizer.paid_status = True
            organizer.save()

            workspace.poll_limit = self.ENTERPRISE_TIER[0]["poll_limit"]
            workspace.voter_limit = self.ENTERPRISE_TIER[0]["voter_limit"]
            workspace.save()

            message = "You have upgraded to Pollar ENTERPRISE package."

            return message

    def current_poll_count(self):

        organizer = self.organizer

        current_count = Poll.objects.filter(organizer=organizer).count()

        return current_count

    def election_completeness(self, tier):

        organizer = self.organizer

        complete_current_count = Poll.objects.filter(organizer=organizer, open=False).count()

        if complete_current_count == tier["poll_limit"]:

            complete = True

        elif complete_current_count < tier["poll_limit"]:

            complete = False

        return complete

class PollAction(AccountObject):

    def __init__(self, workspace, organizer) -> None:
        super().__init__(workspace, organizer)

        self.current_count = self.current_poll_count()
        self.tier = self.check_tier()

    def __str__(self) -> str:
        
        return super().__str__()

    def create_poll(
        self,
        seat,
        intro,
        begin_date,
        end_date
    ):

        organizer = self.organizer
        workspace = self.workspace

        poll_limit = (self.tier[0]["poll_limit"] - 1)

        try:

            assert (self.current_count <= poll_limit), "current_count is greater than poll_limit"

        except AssertionError:

            raise Exception("You have reached the max number of polls you can create given your currently running package. Upgrade to create more polls")

        else:

            new_poll = Poll.objects.create(
                seat=seat,
                intro=intro,
                begin_date=begin_date,
                end_date=end_date,
                organizer=organizer,
                workspace=workspace
            )

        return new_poll

class VoterObject():

    def __init__(self, workspace, user) -> None:

        self.workspace = workspace
        self.user = user

    def __str__(self) -> str:
        
        return f'{self.user.username}: {self.workspace.name}'

    def current_voter_count(self):

        workspace = self.workspace

        current_count = Voter.objects.filter(workspace=workspace).count()

        return current_count

class VoterAction(VoterObject):

    def __init__(self, workspace, user) -> None:
        super().__init__(workspace, user)

        self.voter_count = self.current_voter_count()

    def __str__(self) -> str:

        return super().__str__()

    def register_voter_to_workspace(self, country):

        voter_limit = (self.workspace.voter_limit - 1)

        try:

            assert (self.voter_count <= voter_limit), "current_count is greater than voter_limit"

        except AssertionError:

            raise Exception(f'The max number of voters i.e. {self.workspace.voter_limit} that can be registered to this workspace has already been reached. Contact your organizer for more information.')

        else:

            new_voter = Voter.objects.create(
                user=self.user,
                country=country,
                workspace=self.workspace
            )

        return new_voter