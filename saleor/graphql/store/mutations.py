import graphene

from ...core.permissions import StorePermissions
from ..core.types.common import StoreError
from ...store import models
from ..core.mutations import ModelMutation


class StoreInput(graphene.InputObjectType):
    name = graphene.String(required=True, description="Store name.")
    country = graphene.String(description="Country.")


class StoreCreate(ModelMutation):
    class Arguments:
        input = StoreInput(
            required=True, description="Fields required to create store."
        )

    class Meta:
        description = "Creates new store."
        model = models.Store
        permissions = (StorePermissions.MANAGE_STORES,)
        error_type_class = StoreError
        error_type_field = "store_errors"


class StoreUpdate(ModelMutation):
    class Arguments:
        input = StoreInput(
            required=True, description="Fields required to update store."
        )
        id = graphene.ID(required=True, description="ID of store to update.")

    class Meta:
        description = "Update given store."
        model = models.Store
        permissions = (StorePermissions.MANAGE_STORES,)
        error_type_class = StoreError
        error_type_field = "store_errors"

