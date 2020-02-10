import pytest
import graphene
from django.db import models

from faker import Faker

from saleor.core.permissions import StorePermissions
from saleor.store.models import Store
from tests.api.utils import assert_no_permission, get_graphql_content


fake = Faker()

MUTATION_CREATE_STORE = """
mutation createStore($input: StoreInput!) {
    createStore(input: $input) {
        errors {
            field
            message
        }
        store {
            id
            name
            country {
                code
            }
        }
    }
}
"""


MUTATION_UPDATE_STORE = """
mutation updateStore($id: ID!, $input: StoreInput!) {
    updateStore(id: $id, input: $input) {
        errors {
            field
            message
        }
        store {
            id
            name
            country {
                code
            }
        }
    }
}
"""


QUERY_STORE = """
query store($id: ID!) {
    store(id: $id) {
        name
        country
        users(first:100){
            totalCount
                edges{
                    node{
                        id
                        email
                    }
                }
        }
    }
}
"""


QUERY_STORES = """
    query {
        stores(first:100) {
            totalCount
            edges {
                node {
                    id
                    name
                    country
                    users(first:100){
                        totalCount
                        edges{
                            node{
                                id
                                email
                            }
                        }
                    }
                }
            }
        }
    }
"""

QUERY_STORES_WITH_FILTERS = """
    query stores($filter: StoreFilterInput!) {
        stores(first: 100, filter: $filter) {
            totalCount
            edges {
                node {
                    id
                }
            }
        }
    }
"""


def test_store_cannot_be_created_without_permission(
    staff_api_client
):
    assert not staff_api_client.user.has_perm(StorePermissions.MANAGE_STORES)
    variables = {
        "input": {
            "name": fake.name(),
            "country": 'CN',
        }
    }

    response = staff_api_client.post_graphql(MUTATION_CREATE_STORE, variables=variables)
    assert_no_permission(response)


def test_create_store_mutation(staff_api_client, permission_manage_stores):
    staff_api_client.user.user_permissions.add(permission_manage_stores)
    name = fake.name()
    country = "CN"
    old_store_count = Store.objects.count()

    variables = {
        "input": {
            "name": name,
            "country": "CN",
        }
    }
    response = staff_api_client.post_graphql(MUTATION_CREATE_STORE, variables)
    content = get_graphql_content(response)
    assert Store.objects.count() == old_store_count + 1
    content_errors = content["data"]["createStore"]["errors"]
    assert len(content_errors) == 0
    store = content["data"]["createStore"]["store"]
    assert name == store["name"]
    assert country == store["country"]["code"]


def test_update_store_required_permission(staff_api_client, store):
    assert not staff_api_client.user.has_perm(StorePermissions.MANAGE_STORES)
    store_id = graphene.Node.to_global_id("StoreType", store.pk)
    name = fake.name()
    country = store.country.code

    variables = {
        "id": store_id,
        "input": {
            "name": name,
            "country": country,
        },
    }
    response = staff_api_client.post_graphql(MUTATION_UPDATE_STORE, variables=variables)
    assert_no_permission(response)


def test_update_store_mutation(staff_api_client, permission_manage_stores, store):
    staff_api_client.user.user_permissions.add(permission_manage_stores)
    store_id = graphene.Node.to_global_id("StoreType", store.pk)
    name = fake.name()
    country = store.country.code

    variables = {
        "id": store_id,
        "input": {
            "name": name,
            "country": country,
        },
    }
    response = staff_api_client.post_graphql(
        MUTATION_UPDATE_STORE, variables=variables,
    )
    content = get_graphql_content(response)
    content_errors = content["data"]["updateStore"]["errors"]
    assert len(content_errors) == 0
    store.refresh_from_db()
    assert store.name == name


def test_query_store_requires_permission(staff_api_client, store):
    assert not staff_api_client.user.has_perm(StorePermissions.MANAGE_STORES)
    store_id = graphene.Node.to_global_id("StoreType", store.pk)
    response = staff_api_client.post_graphql(QUERY_STORE, variables={"id": store_id})
    assert_no_permission(response)


def test_query_store(staff_api_client, store, permission_manage_stores):
    staff_api_client.user.user_permissions.add(permission_manage_stores)
    store_id = graphene.Node.to_global_id("StoreType", store.pk)
    response = staff_api_client.post_graphql(QUERY_STORE, variables={"id": store_id})
    content = get_graphql_content(response)
    content_store = content["data"]["store"]
    # TODO: test by leonard!!
    #assert (
    #    content_store["users"]["totalCount"]
    #    == len(store.users)
    #)
    assert content_store["name"] == store.name
    assert content_store["country"] == store.country.code


def test_query_stores_requires_permissions(staff_api_client):
    assert not staff_api_client.user.has_perm(StorePermissions.MANAGE_STORES)
    response = staff_api_client.post_graphql(QUERY_STORES)
    assert_no_permission(response)


def test_query_stores(staff_api_client, store, permission_manage_stores):
    staff_api_client.user.user_permissions.add(permission_manage_stores)
    response = staff_api_client.post_graphql(QUERY_STORES)
    content = get_graphql_content(response)
    total_count = content["data"]["stores"]["totalCount"]
    assert total_count == Store.objects.count()


@pytest.mark.skip()
def test_query_stores_with_filters_country(
    staff_api_client, store, permission_manage_stores
):
    staff_api_client.user.user_permissions.add(permission_manage_stores)
    country = store.country.code
    response_name = staff_api_client.post_graphql(
        QUERY_STORES_WITH_FILTERS, variables={"filter": {"search": country}}
    )
    content = get_graphql_content(response_name)
    total_count = content["data"]["stores"]["totalCount"]
    assert total_count == Store.objects.filter(country=country).count()
