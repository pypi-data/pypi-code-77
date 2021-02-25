# Copyright 2020 Camptocamp SA (http://www.camptocamp.com)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from .common import CommonCase
from .common_misc import MenuTestMixin


class UserCase(CommonCase, MenuTestMixin):
    @classmethod
    def setUpClassVars(cls, *args, **kwargs):
        super().setUpClassVars(*args, **kwargs)
        cls.profile = cls.env.ref("shopfloor_base.profile_demo_1")
        cls.profile2 = cls.env.ref("shopfloor_base.profile_demo_2")

    def setUp(self):
        super().setUp()
        with self.work_on_services(profile=self.profile) as work:
            self.service = work.component(usage="user")

    def test_menu_no_profile(self):
        """Request /user/menu"""
        # Simulate the client asking the menu
        response = self.service.dispatch("menu")
        menus = self.env["shopfloor.menu"].search([])
        self.assert_response(
            response,
            data={"menus": [self._data_for_menu_item(menu) for menu in menus]},
        )

    def test_menu_by_profile(self):
        """Request /user/menu w/ a specific profile"""
        # Simulate the client asking the menu
        menus = self.env["shopfloor.menu"].sudo().search([])
        menu = menus[0]
        menu.profile_id = self.profile
        (menus - menu).profile_id = self.profile2

        response = self.service.dispatch("menu")
        self.assert_response(
            response, data={"menus": [self._data_for_menu_item(menu)]},
        )

    def test_user_info(self):
        """Request /user/user_info"""
        response = self.service.dispatch("user_info")
        self.assert_response(
            response,
            data={"user_info": {"id": self.env.user.id, "name": self.env.user.name}},
        )
