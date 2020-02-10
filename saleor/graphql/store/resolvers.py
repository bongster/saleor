import graphene
from graphql_jwt.exceptions import PermissionDenied

from ...core.permissions import StorePermissions
from ...store import models
from ..utils import sort_queryset
# from .sorters import StoreSortField
from .types import StoreType

def resolve_store(info, store_id):
    print(store_id)
    store = graphene.Node.get_node_from_global_id(info, store_id)
    return store


def resolve_stores():
    qs = models.Store.objects.all()
    return qs
