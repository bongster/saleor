import graphene
import graphene_django_optimizer as gql_optimizer
from django_countries import countries

from ..core.connection import CountableDjangoObjectType
from ..core.fields import PrefetchingConnectionField
from ..account.types import User
from ...store import models


class StoreType(CountableDjangoObjectType):
    users = gql_optimizer.field(
        PrefetchingConnectionField(
            User, description="List of user."
        ),
    )

    class Meta:
        description = "Store object."
        model = models.Store
        interfaces = [graphene.relay.Node]
        name = 'StoreType'

    @staticmethod
    def resolve_users(root:models.Store, info, **_kwargs):
        qs = root.users.all()
        return gql_optimizer.query(qs, info)
