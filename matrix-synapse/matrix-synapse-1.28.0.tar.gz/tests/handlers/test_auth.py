# -*- coding: utf-8 -*-
# Copyright 2015, 2016 OpenMarket Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from mock import Mock

import pymacaroons

from synapse.api.errors import AuthError, ResourceLimitError

from tests import unittest
from tests.test_utils import make_awaitable


class AuthTestCase(unittest.HomeserverTestCase):
    def prepare(self, reactor, clock, hs):
        self.auth_handler = hs.get_auth_handler()
        self.macaroon_generator = hs.get_macaroon_generator()

        # MAU tests
        # AuthBlocking reads from the hs' config on initialization. We need to
        # modify its config instead of the hs'
        self.auth_blocking = hs.get_auth()._auth_blocking
        self.auth_blocking._max_mau_value = 50

        self.small_number_of_users = 1
        self.large_number_of_users = 100

    def test_token_is_a_macaroon(self):
        token = self.macaroon_generator.generate_access_token("some_user")
        # Check that we can parse the thing with pymacaroons
        macaroon = pymacaroons.Macaroon.deserialize(token)
        # The most basic of sanity checks
        if "some_user" not in macaroon.inspect():
            self.fail("some_user was not in %s" % macaroon.inspect())

    def test_macaroon_caveats(self):
        token = self.macaroon_generator.generate_access_token("a_user")
        macaroon = pymacaroons.Macaroon.deserialize(token)

        def verify_gen(caveat):
            return caveat == "gen = 1"

        def verify_user(caveat):
            return caveat == "user_id = a_user"

        def verify_type(caveat):
            return caveat == "type = access"

        def verify_nonce(caveat):
            return caveat.startswith("nonce =")

        v = pymacaroons.Verifier()
        v.satisfy_general(verify_gen)
        v.satisfy_general(verify_user)
        v.satisfy_general(verify_type)
        v.satisfy_general(verify_nonce)
        v.verify(macaroon, self.hs.config.macaroon_secret_key)

    def test_short_term_login_token_gives_user_id(self):
        token = self.macaroon_generator.generate_short_term_login_token("a_user", 5000)
        user_id = self.get_success(
            self.auth_handler.validate_short_term_login_token_and_get_user_id(token)
        )
        self.assertEqual("a_user", user_id)

        # when we advance the clock, the token should be rejected
        self.reactor.advance(6)
        self.get_failure(
            self.auth_handler.validate_short_term_login_token_and_get_user_id(token),
            AuthError,
        )

    def test_short_term_login_token_cannot_replace_user_id(self):
        token = self.macaroon_generator.generate_short_term_login_token("a_user", 5000)
        macaroon = pymacaroons.Macaroon.deserialize(token)

        user_id = self.get_success(
            self.auth_handler.validate_short_term_login_token_and_get_user_id(
                macaroon.serialize()
            )
        )
        self.assertEqual("a_user", user_id)

        # add another "user_id" caveat, which might allow us to override the
        # user_id.
        macaroon.add_first_party_caveat("user_id = b_user")

        self.get_failure(
            self.auth_handler.validate_short_term_login_token_and_get_user_id(
                macaroon.serialize()
            ),
            AuthError,
        )

    def test_mau_limits_disabled(self):
        self.auth_blocking._limit_usage_by_mau = False
        # Ensure does not throw exception
        self.get_success(
            self.auth_handler.get_access_token_for_user_id(
                "user_a", device_id=None, valid_until_ms=None
            )
        )

        self.get_success(
            self.auth_handler.validate_short_term_login_token_and_get_user_id(
                self._get_macaroon().serialize()
            )
        )

    def test_mau_limits_exceeded_large(self):
        self.auth_blocking._limit_usage_by_mau = True
        self.hs.get_datastore().get_monthly_active_count = Mock(
            return_value=make_awaitable(self.large_number_of_users)
        )

        self.get_failure(
            self.auth_handler.get_access_token_for_user_id(
                "user_a", device_id=None, valid_until_ms=None
            ),
            ResourceLimitError,
        )

        self.hs.get_datastore().get_monthly_active_count = Mock(
            return_value=make_awaitable(self.large_number_of_users)
        )
        self.get_failure(
            self.auth_handler.validate_short_term_login_token_and_get_user_id(
                self._get_macaroon().serialize()
            ),
            ResourceLimitError,
        )

    def test_mau_limits_parity(self):
        # Ensure we're not at the unix epoch.
        self.reactor.advance(1)
        self.auth_blocking._limit_usage_by_mau = True

        # Set the server to be at the edge of too many users.
        self.hs.get_datastore().get_monthly_active_count = Mock(
            return_value=make_awaitable(self.auth_blocking._max_mau_value)
        )

        # If not in monthly active cohort
        self.get_failure(
            self.auth_handler.get_access_token_for_user_id(
                "user_a", device_id=None, valid_until_ms=None
            ),
            ResourceLimitError,
        )
        self.get_failure(
            self.auth_handler.validate_short_term_login_token_and_get_user_id(
                self._get_macaroon().serialize()
            ),
            ResourceLimitError,
        )

        # If in monthly active cohort
        self.hs.get_datastore().user_last_seen_monthly_active = Mock(
            return_value=make_awaitable(self.clock.time_msec())
        )
        self.get_success(
            self.auth_handler.get_access_token_for_user_id(
                "user_a", device_id=None, valid_until_ms=None
            )
        )
        self.get_success(
            self.auth_handler.validate_short_term_login_token_and_get_user_id(
                self._get_macaroon().serialize()
            )
        )

    def test_mau_limits_not_exceeded(self):
        self.auth_blocking._limit_usage_by_mau = True

        self.hs.get_datastore().get_monthly_active_count = Mock(
            return_value=make_awaitable(self.small_number_of_users)
        )
        # Ensure does not raise exception
        self.get_success(
            self.auth_handler.get_access_token_for_user_id(
                "user_a", device_id=None, valid_until_ms=None
            )
        )

        self.hs.get_datastore().get_monthly_active_count = Mock(
            return_value=make_awaitable(self.small_number_of_users)
        )
        self.get_success(
            self.auth_handler.validate_short_term_login_token_and_get_user_id(
                self._get_macaroon().serialize()
            )
        )

    def _get_macaroon(self):
        token = self.macaroon_generator.generate_short_term_login_token("user_a", 5000)
        return pymacaroons.Macaroon.deserialize(token)
