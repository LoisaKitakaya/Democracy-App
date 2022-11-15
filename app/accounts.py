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
            {"name": self.FREE, "poll_limit": 2, "voter_limit": 10},
        )

        self.PRO_TIER = (
            {"tier_name": self.PRO, "poll_limit": 4, "voter_limit": 100},
        )

        self.BUSINESS_TIER = (
            {"tier_name": self.BUSINESS, "poll_limit": 8, "voter_limit": 1000},
        )

        self.ENTERPRISE_TIER = (
            {"tier_name": self.ENTERPRISE, "poll_limit": 16, "voter_limit": 10000},
        )

    def __str__(self) -> str:
        
        return f'[{self.organizer.user.username}: {self.workspace.name}]'

    def check_tier(self):

        tier = self.organizer.running_package

        poll_limit = self.workspace.poll_limit
        voter_limit = self.workspace.voter_limit

        if tier == self.FREE_TIER[0].get("tier_name") and poll_limit == self.FREE_TIER[0].get("poll_limit") and voter_limit == self.FREE_TIER[0].get("voter_limit"):

            account_tier = self.FREE_TIER

            return account_tier

        elif tier == self.PRO_TIER[0].get("tier_name") and poll_limit == self.PRO_TIER[0].get("poll_limit") and voter_limit == self.PRO_TIER[0].get("voter_limit"):

            account_tier = self.PRO_TIER

            return account_tier

        elif tier == self.BUSINESS_TIER[0].get("tier_name") and poll_limit == self.BUSINESS_TIER[0].get("poll_limit") and voter_limit == self.BUSINESS_TIER[0].get("voter_limit"):

            account_tier = self.BUSINESS_TIER

            return account_tier

        elif tier == self.ENTERPRISE_TIER[0].get("tier_name") and poll_limit == self.ENTERPRISE_TIER[0].get("poll_limit") and voter_limit == self.ENTERPRISE_TIER[0].get("voter_limit"):

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

            workspace.poll_limit = self.pro["poll_limit"]
            workspace.voter_limit = self.pro["voter_limit"]
            workspace.save()

            message = "You have upgraded to Pollar PRO package."

            return message

        elif tier == "BUSINESS_TIER":

            organizer = self.organizer
            workspace = self.workspace

            organizer.running_package = self.BUSINESS
            organizer.paid_status = True
            organizer.save()

            workspace.poll_limit = self.business["poll_limit"]
            workspace.voter_limit = self.business["voter_limit"]
            workspace.save()

            message = "You have upgraded to Pollar BUSINESS package."

            return message

        elif tier == "ENTERPRISE_TIER":

            organizer = self.organizer
            workspace = self.workspace

            organizer.running_package = self.ENTERPRISE
            organizer.paid_status = True
            organizer.save()

            workspace.poll_limit = self.enterprise["poll_limit"]
            workspace.voter_limit = self.enterprise["voter_limit"]
            workspace.save()

            message = "You have upgraded to Pollar ENTERPRISE package."

            return message

    def current_poll_count(self):

        organizer = self.organizer

        current_count = Poll.objects.filter(organizer=organizer).count()

        return current_count

    def current_voter_count(self):

        workspace = self.workspace

        current_count = Voter.objects.filter(workspace=workspace).count()

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

        current_count = self.current_poll_count()
        tier = self.check_tier()

        poll_limit = (tier[0].get("poll_limit") + 1)

        try:

            assert (current_count <= poll_limit), "current_count is greater than poll_limit"

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
