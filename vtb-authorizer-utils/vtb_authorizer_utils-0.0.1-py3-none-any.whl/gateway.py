from typing import Dict, Any, Optional, List, FrozenSet, Callable

from vtb_http_interaction.keycloak_gateway import KeycloakConfig
from vtb_http_interaction.services import AuthorizationService

from vtb_authorizer_utils.converters import convert_user, convert_organization, convert_project, \
    convert_folder, convert_children
from vtb_authorizer_utils.data_objects import User, Organization, Project, Folder, Children
from vtb_authorizer_utils.errors import NotAllowedParameterError


class AuthorizerGateway:
    def __init__(self, base_url: str,
                 keycloak_config: KeycloakConfig,
                 redis_connection_string: str,
                 access_token: Optional[str] = None):
        self.base_url = base_url
        self.keycloak_config = keycloak_config
        self.redis_connection_string = redis_connection_string
        self.access_token = access_token

    """"""""" Пользователи """""""""

    async def get_user(self, keycloak_id: str) -> Optional[User]:
        """ Получение пользователя по keycloak_id (Keycloak ID) """
        return await self._get_item([_users_url], keycloak_id, convert_user)

    async def get_users(self, **query_params) -> Optional[List[User]]:
        """ Получение списка пользователей """
        _check_request(query_params, _users_allowed_parameters)

        return await self._get_list([_users_url], convert_user, **query_params)

    """"""""" Организации """""""""

    async def get_organization(self, name: str) -> Optional[Organization]:
        """ Получение организации по name (кодовое название) """
        return await self._get_item([_organizations_url], name, convert_organization)

    async def get_organizations(self, **query_params) -> Optional[List[Organization]]:
        """ Получение списка организаций """
        _check_request(query_params, _organizations_allowed_parameters)

        return await self._get_list([_organizations_url], convert_organization, **query_params)

    async def get_organization_projects(self, name: str, **query_params) -> Optional[List[Project]]:
        """ Получение проектов организации """
        _check_request(query_params, _organization_projects_allowed_parameters)

        return await self._get_list([_organizations_url, name, _projects_url], convert_project,
                                    **query_params)

    async def get_organization_children(self, name: str, **query_params) -> Optional[List[Children]]:
        """ Получение потомков организации """

        return await self._get_list([_organizations_url, name, 'children'], convert_children,
                                    **query_params)

    """"""""" Folders """""""""

    async def get_folder(self, name: str) -> Optional[Folder]:
        """ Получение папки по name """
        return await self._get_item([_folders_url], name, convert_folder)

    """"""""" Projects """""""""

    async def get_project(self, name: str) -> Optional[Project]:
        """ Получение проекта по name """
        return await self._get_item([_projects_url], name, convert_project)

    """"""""" private """""""""

    async def _get_item(self, url_path: List[str], item_id: Any, converter: Callable[[Dict[str, Any]], Any]) -> \
            Optional[Any]:
        """ Получение объекта """
        status, response = await self._create_service(url_path).get(item_id=item_id)
        if status == 200:
            return converter(response['data'])

        return None

    async def _get_list(self, url_path: List[str], converter: Callable[[Dict[str, Any]], Any],
                        **query_params) -> Optional[List]:
        """ Получение списка объектов """

        headers = {'Authorization': f'Bearer {self.access_token}'} if self.access_token else {}

        status, response = await self._create_service(url_path).get(cfg={'params': query_params, 'headers': headers})

        if status == 200:
            return list(map(converter, response['data']))

        return None

    def _create_service(self, url_path: List[str]) -> AuthorizationService:
        """ Создание объекта AuthorizationService """
        url = _join_str(self.base_url, *url_path)

        return AuthorizationService(url,
                                    self.keycloak_config,
                                    self.redis_connection_string)


_users_allowed_parameters = frozenset({"page", "per_page", "q", "username", "firstname", "lastname", "email"})
_users_url = 'users'

_organizations_allowed_parameters = frozenset({"page", "per_page", "include"})
_organization_projects_allowed_parameters = frozenset({"page", "per_page", "include"})
_organizations_url = 'organizations'

_folders_url = 'folders'
_projects_url = 'projects'


def _check_request(query_params: Dict[str, Any], allowed_parameters: FrozenSet[str]):
    """Проверка параметров запроса"""
    keys = frozenset(query_params.keys())
    not_allowed_parameters = keys - allowed_parameters
    if len(not_allowed_parameters) > 0:
        raise NotAllowedParameterError(not_allowed_parameters, _users_allowed_parameters)


def _join_str(*args, sep: Optional[str] = '/') -> str:
    return sep.join(arg.strip(sep) for arg in args)
