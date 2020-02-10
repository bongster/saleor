import graphene

from ...core.permissions import StorePermissions
from ..core.fields import BaseDjangoConnectionField
from ..decorators import permission_required
from ..core.fields import FilterInputConnectionField
from .mutations import StoreCreate, StoreUpdate
from .resolvers import (
    resolve_store,
    resolve_stores,
)
from .types import StoreType


class StoreQueries(graphene.ObjectType):
    store = graphene.Field(
        StoreType,
        id=graphene.Argument(
            graphene.ID, required=True, description="ID of the stock."
        ),
        description="Look up a store by ID."
    )

    stores = FilterInputConnectionField(
        StoreType,
        description="List of stores."
    )


    @permission_required(StorePermissions.MANAGE_STORES)
    def resolve_stores(self, *_args, **_kwargs):
        return resolve_stores()

    @permission_required(StorePermissions.MANAGE_STORES)
    def resolve_store(self, info, id):
        return resolve_store(info, id)


class StoreMutations(graphene.ObjectType):
    create_store = StoreCreate.Field()
    update_store = StoreUpdate.Field()
