import time

from loguru import logger


class MCDatabasesFinder:
    @logger.catch
    def __init__(self, username_databases: list[dict]) -> None:
        self.username_databases: list[dict] = username_databases

        # Sort the databases by name
        start_time: float = time.time()
        logger.info('Sorting the databases by name')
        self.username_databases.sort(key=lambda x: x.get('username', '').lower())
        logger.info(f'Sorted the databases by name in {time.time() - start_time:.2f} seconds')

    @logger.catch
    def search(self, name: str) -> list:
        """
        Search the usernames in the databases using binary search
        :param name:  The name to search
        :return: The databases that match the name
        """
        left: int = 0
        right: int = len(self.username_databases) - 1
        results: list = []

        while left <= right:
            mid: int = (left + right) // 2
            current_name: str = self.username_databases[mid].get('username').lower()

            if current_name == name.lower():
                results.append(self.username_databases[mid])
                idx: int = mid - 1

                while idx >= 0 and self.username_databases[idx].get('username').lower() == name.lower():
                    results.append(self.username_databases[idx])
                    idx -= 1

                idx: int = mid + 1

                while idx < len(self.username_databases) and self.username_databases[idx].get('username').lower() == name.lower():
                    results.append(self.username_databases[idx])
                    idx += 1

                return results

            elif current_name < name.lower():
                left: int = mid + 1

            else:
                right: int = mid - 1

        return results
