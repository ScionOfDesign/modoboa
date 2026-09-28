"""Tests for authentication backend helpers."""

from django.test import TestCase

from modoboa.core import factories as core_factories
from modoboa.lib.authbackends import apply_default_domain


class ApplyDefaultDomainTestCase(TestCase):
    """Default domain is appended only for non-local, domain-less names."""

    def test_appends_domain_when_username_has_none(self):
        self.assertEqual(
            apply_default_domain("scion", "studiowhy.net"),
            "scion@studiowhy.net",
        )

    def test_leaves_username_that_already_has_a_domain(self):
        self.assertEqual(
            apply_default_domain("scion@other.net", "studiowhy.net"),
            "scion@other.net",
        )

    def test_leaves_local_account_unchanged(self):
        core_factories.UserFactory(username="admin", is_local=True)
        self.assertEqual(
            apply_default_domain("admin", "studiowhy.net"),
            "admin",
        )
        self.assertEqual(
            apply_default_domain("Admin", "studiowhy.net"),
            "Admin",
        )

    def test_appends_domain_for_non_local_account(self):
        core_factories.UserFactory(username="scion", is_local=False)
        self.assertEqual(
            apply_default_domain("scion", "studiowhy.net"),
            "scion@studiowhy.net",
        )

    def test_disabled_when_domain_is_empty(self):
        self.assertEqual(apply_default_domain("scion", ""), "scion")
        self.assertEqual(apply_default_domain("scion", None), "scion")

    def test_strips_a_leading_at_sign(self):
        self.assertEqual(
            apply_default_domain("scion", "@studiowhy.net"),
            "scion@studiowhy.net",
        )
