from polls.models import Poll
from voters.models import Voter

class AccountObject():

    def __init__(self, workspace, organizer) -> None:

        self.free = {
            "tier_name": "Free",
            "poll_limit": 2,
            "voter_limit": 10
        }

        self.pro = {
            "tier_name": "Pro",
            "poll_limit": 4,
            "voter_limit": 100
        }

        self.business = {
            "tier_name": "Business",
            "poll_limit": 8,
            "voter_limit": 1000
        }

        self.enterprise = {
            "tier_name": "Enterprise",
            "poll_limit": 16,
            "voter_limit": 10000
        }

        self.FREE = 'FREE_TIER'
        self.PRO = 'PRO_TIER'
        self.BUSINESS = 'BUSINESS_TIER'
        self.ENTERPRISE = 'ENTERPRISE_TIER'

        self.workspace = workspace

        self.organizer = organizer

    def __str__(self) -> str:
        
        return f'[{self.organizer.user.username}: {self.workspace.name}]'

    def check_tier(self):

        tier = self.organizer.running_package

        poll_limit = self.workspace.poll_limit
        voter_limit = self.workspace.voter_limit

        if tier == "FREE_TIER" and poll_limit == 2 and voter_limit == 10:

            return self.free

        elif tier == "PRO_TIER" and poll_limit == 6 and voter_limit == 100:

            return self.pro

        elif tier == "BUSINESS_TIER" and poll_limit == 12 and voter_limit == 1000:

            return self.business

        elif tier == "ENTERPRISE_TIER" and poll_limit == 24 and voter_limit == 10000:

            return self.enterprise

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

        print(current_count, tier["poll_limit"], type(tier["poll_limit"]))

        if current_count >= tier["poll_limit"]:

            return None

        elif current_count < tier["poll_limit"]:

            new_poll = Poll.objects.create(
                seat=seat,
                intro=intro,
                begin_date=begin_date,
                end_date=end_date,
                organizer=organizer,
                workspace=workspace
            )

        return new_poll
