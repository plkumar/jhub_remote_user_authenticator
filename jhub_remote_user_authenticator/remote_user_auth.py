
import os
from jupyterhub.handlers import BaseHandler
from jupyterhub.auth import Authenticator
from jupyterhub.auth import LocalAuthenticator
from jupyterhub.utils import url_path_join
from tornado import gen, web
from traitlets import Unicode
from urllib.parse import unquote
from urllib.parse import urlparse
from urllib.parse import parse_qs


class RemoteUserLoginHandler(BaseHandler):

    def get(self):
        header_name = self.authenticator.header_name
        print("Header name", header_name)
        # print("Request headers", self.request.headers)
        remote_user = self.request.headers.get(header_name, "")
        print("Remote user", remote_user)
        
        # if remote_user == "":
        #     # remote_user =  ''.join(self.request.query_arguments.get('username', ""))
        #     print(self.request.full_url())
        #     if self.request.query_arguments.get('next') != None:
        #         try:
        #             next_url=parse_qs(urlparse(self.request.full_url()).query)["next"][0]
        #             print(next_url)
        #             remote_user = parse_qs(urlparse(next_url).query)["username"][0]
        #             print("Remoteuser", remote_user)
        #         except:
        #             remote_user = ""
        #     else:
        #         remote_user = ''.join([byte_array.decode('utf-8') for byte_array in self.request.query_arguments.get('username', "")])

        if remote_user == "":
            raise web.HTTPError(401)
        
        if(remote_user.find("@")):
            remote_user = unquote(remote_user).split("@")[0] 
        print("Cleaned Remote user", remote_user)
        user = self.user_from_username(remote_user)
        self.set_login_cookie(user)
        next_url = self.get_next_url(user)
        self.redirect(next_url)


class RemoteUserAuthenticator(Authenticator):
    """
    Accept the authenticated user name from the REMOTE_USER HTTP header.
    """
    header_name = Unicode(
        default_value='REMOTE_USER',
        config=True,
        help="""HTTP header to inspect for the authenticated username.""")

    def get_handlers(self, app):
        return [
            (r'/login', RemoteUserLoginHandler),
        ]

    @gen.coroutine
    def authenticate(self, *args):
        raise NotImplementedError()


class RemoteUserLocalAuthenticator(LocalAuthenticator):
    """
    Accept the authenticated user name from the REMOTE_USER HTTP header.
    Derived from LocalAuthenticator for use of features such as adding
    local accounts through the admin interface.
    """
    header_name = Unicode(
        default_value='REMOTE_USER',
        config=True,
        help="""HTTP header to inspect for the authenticated username.""")

    def get_handlers(self, app):
        return [
            (r'/login', RemoteUserLoginHandler),
        ]

    @gen.coroutine
    def authenticate(self, *args):
        raise NotImplementedError()
