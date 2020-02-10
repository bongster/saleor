import pytest
from faker import Faker

from saleor.store.models import Store

fake = Faker()

def test_success_create_store(customer_user):
    store = Store(
        name=fake.name(),
        country = 'CN'
    )
    store.save()
    assert store.id
    assert store.country == 'CN'
    assert store.users
    store.users.add(customer_user)
    assert store.users.count() == 1
    updated_store = Store.objects.get(pk=store.id)
    assert updated_store.users.count() == 1
