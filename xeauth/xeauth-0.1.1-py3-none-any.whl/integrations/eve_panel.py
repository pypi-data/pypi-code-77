
import param
import panel as pn

from ..oauth import NotebookSession
try:
    from eve_panel.auth import EveAuthBase
except ImportError:
    pass

class XenonEveAuth(EveAuthBase):
    session = param.ClassSelector(NotebookSession, default=NotebookSession())

    def get_headers(self):
        """Generate auth headers for HTTP requests.

        Returns:
            dict: Auth related headers to be included in all requests.
        """
        if self.logged_in:
            return {"Authorization": f"Bearer {self.session.access_token}"}
        else:
            return {}

    def login(self):
        """perform any actions required to aquire credentials.

        Returns:
            bool: whether login was successful
        """
        self.session.login_requested(None)

    def logout(self):
        """perform any actions required to logout.

        Returns:
            bool: whether login was successful
        """
        return self.session.logout()

    @property
    def logged_in(self):
        return self.session.logged_in

    def set_credentials(self, **credentials):
        """Set the access credentials manually.
        """
        for k,v in credentials.items():
            setattr(self.session, k, v)
    
    def credentials_view(self):
        return self.session.gui
