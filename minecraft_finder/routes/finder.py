from fastapi import APIRouter, Response, Request
from loguru import logger

from ..databases import MCDatabasesFinder
from ..utils.obfuscator import ObfuscatorUtils
from ..constants import ObfuscatorConstants

router: APIRouter = APIRouter()


class FinderRouter:
    @logger.catch
    def __init__(self, databases_finder: MCDatabasesFinder):
        self.prefix: str = '/finder'
        self.router: APIRouter = router
        self.databases_finder = databases_finder
        self.obfuscator: ObfuscatorUtils = ObfuscatorUtils(key=ObfuscatorConstants.KEY)
        self._add_routes()
        logger.info(f'Added routes for {self.__class__.__name__}')

    @logger.catch
    def _add_routes(self) -> None:
        """Add routes to the FastAPI application."""
        @self.router.get('/username/{username}', tags=['finder'])
        def search_username(
            request: Request,
            response: Response,
            username: str,
        ):
            """
            Search for a username in the databases.
            :param request: Request object from FastAPI
            :param response: Response object from FastAPI
            :param username: Username to search
            """
            client_ip: str = request.headers.get('X-Forwarded-For')

            if client_ip:
                client_ip = client_ip.split(',')[0].strip()

            else:
                client_ip = request.client.host

            result = self.databases_finder.search(username)
            return {'message': 'User search completed!', 'result': self.obfuscator.obfuscate(str(result))}