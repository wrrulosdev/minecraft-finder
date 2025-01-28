import os
import time
from typing import Union
from concurrent.futures import ThreadPoolExecutor, as_completed

import orjson
from loguru import logger


class MCDatabasesLoader:
    def __init__(self) -> None:
        self.databases_folder_path: str = 'databases/'

        if not os.path.exists(self.databases_folder_path):
            logger.critical(f'Databases folder not found: {self.databases_folder_path}.')

    @logger.catch
    def load_single_database(self, database_file: str) -> tuple[list, int]:
        """
        Load a single database file
        :param database_file: The database file to load
        :return: The loaded database
        """
        username_databases: list = []
        data_count: int = 0
        start_time: float = time.time()

        try:
            logger.info(f'Loading database file: {database_file}')

            with open(os.path.join(self.databases_folder_path, database_file), 'rb') as file:
                data: list = orjson.loads(file.read())
                username_databases = [item for item in data if 'username' in item]
                data_count = len(data)

            logger.info(f'Loaded {data_count} data in {time.time() - start_time:.2f} seconds from {database_file}')

        except orjson.JSONDecodeError:
            logger.error(f'Error loading database file: {database_file} (Invalid JSON)')

        except UnicodeError:
            logger.error(f'Error loading database file: {database_file} (Invalid encoding)')

        except Exception as e:
            logger.error(f'Unexpected error loading {database_file}: {e}')

        return username_databases, data_count

    @logger.catch
    def load_databases(self, limit: Union[int, None] = None) -> tuple[list, int]:
        """
        Load the databases from the databases folder
        :param limit: Limit the number of databases to load
        :return: The loaded databases
        """
        database_files: list = os.listdir(self.databases_folder_path)

        if limit is not None:
            database_files = database_files[:limit]

        username_databases: list = []
        total_data_count: int = 0
        start_time: float = time.time()
        logger.info(f'Loading databases from {self.databases_folder_path}')

        with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            futures = [executor.submit(self.load_single_database, db_file) for db_file in database_files]

            for future in as_completed(futures):
                try:
                    u_db, count = future.result()
                    username_databases.extend(u_db)
                    total_data_count += count

                except Exception as e:
                    logger.error(f"Error processing a database file: {e}")

        logger.info(f'Loaded {total_data_count} data in {time.time() - start_time:.2f} seconds. {len(username_databases)} usernames found')
        return username_databases, total_data_count
