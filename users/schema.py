import graphene
from graphene_django import DjangoObjectType
from users.models import User

# my object type

class UserType(DjangoObjectType):

    class Meta:

        model = User

        fields = '__all__'

# GraphQL Queries

class Query(graphene.ObjectType):
    
    pass

# User model mutations

class UserRegistration(graphene.Mutation):

    class Arguments:

        username = graphene.String(required=True)
        email = graphene.String(required=True)
        firstname = graphene.String(required=True)
        lastname = graphene.String(required=True)
        password = graphene.String(required=True)
        password2 = graphene.String(required=True)

    user = graphene.Field(UserType)

    @classmethod
    def mutate(
        cls, root, info, 
        username, 
        email, 
        firstname, 
        lastname, 
        password, 
        password2
        ):

        if not User.objects.filter(email=email).exists():

            if len(password) > 8 and len(password2) > 8:

                if password == password2:

                    user = User.objects.create(
                        username=username, 
                        email=email, 
                        first_name=firstname, 
                        last_name=lastname
                        )

                else:

                    raise Exception("Passwords provided did not match!")

                new_user = User.objects.get(email=email)

                new_user.set_password(password)

                new_user.save()

            else:

                raise Exception("Your password is too short. Must have minimum of 8 characters")

        else:

            raise Exception("A user with the same email already exists. Make sure your email is unique!")

        return UserRegistration(user=user)

# GraphQL Mutations

class Mutation(graphene.ObjectType):
    
    register_user = UserRegistration.Field()