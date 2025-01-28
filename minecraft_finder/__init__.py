import subprocess
import asyncio
import sys
from typing import Optional

import uvicorn
from loguru import logger
from fastapi import FastAPI

from .databases import MCDatabasesLoader, MCDatabasesFinder
from .routes import FinderRouter

logger.add(
    'logs.log', 
    rotation='100 MB',
    retention='31 days',
    compression='zip'
) 


class MinecraftFinderAPI:
    def __init__(self, databases_limit: Optional[int] = None) -> None:    
        subprocess.run('clear || cls', shell=True)
        self.databases_limit: Optional[int] = databases_limit
        self.databases: Optional[tuple] = None
        self._app: FastAPI = FastAPI(
            docs_url='/docs',
            redoc_url='/redoc',
            openapi_url='/openapi.json'
        )
        self._load()
        self._setup_routes([
            FinderRouter
        ])
    
    @logger.catch
    def _load(self) -> None:
        try:
            self.databases = MCDatabasesLoader().load_databases(limit=self.databases_limit)
        
            if self.databases is None:
                logger.critical('No databases found. Exiting..')
                
            self.username_databases: list = self.databases[0]
            self.data_count: int = self.databases[1]
            self.databases_finder: MCDatabasesFinder = MCDatabasesFinder(self.username_databases)
        
        except KeyboardInterrupt:
            logger.info('Stopping..')
            
    @logger.catch
    def _setup_routes(self, router_classes: list) -> None:
        """
        Setup routes for the FastAPI application.
        :param router_classes: Router classes to include in the FastAPI application.
        """
        for router_class in router_classes:
            router_instance = router_class(databases_finder=self.databases_finder)
            self._app.include_router(router_instance.router, prefix=router_instance.prefix)

    @logger.catch
    def run(self):
        """ Run the FastAPI app """
        try:
            uvicorn.run(self._app, host='0.0.0.0', port=8000)
            
        except KeyboardInterrupt:
            logger.info('Shutting down the server...')
            sys.exit(0)
