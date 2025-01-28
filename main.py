import sys
from typing import Optional


from minecraft_finder import MinecraftFinderAPI


if __name__ == '__main__':
    limit: Optional[int] = None
    
    if len(sys.argv) > 1:
        try:
            limit: int = int(sys.argv[1])
            
        except ValueError:
            print('Invalid limit value. Please provide a valid number as a limit!')
            

    mc_finder: MinecraftFinderAPI = MinecraftFinderAPI(databases_limit=limit)
    mc_finder.run()
