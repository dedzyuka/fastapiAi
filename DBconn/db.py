from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine,AsyncEngine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
import os
from typing import AsyncGenerator

DATABASE_URL = "postgresql+asyncpg://postgres:password123@localhost:5433/vectordb"
class DatabaseHalper:
    def __init__(self,
                url : str,
                 echo : bool = False,
                 echo_pool :bool = False,
                 pool_size : int = 5,
                 max_overflow : int = 10):
            self.engine : AsyncEngine = create_async_engine(url=url,
                                                            echo=echo,
                                                            echo_pool = echo_pool,
                                                            pool_size = pool_size,
                                                            max_overflow = max_overflow)    
            self. sessio_factory:async_sessionmaker[AsyncSession] = async_sessionmaker(
                 bind= self.engine,
                 autoflush=False,
                 autocommit = False,
                 expire_on_commit=False,
            )

    

    async def dispose(self)-> None:
        await self.engine.dispose()

    async def session_getter(self)-> AsyncGenerator[AsyncSession,None]:
         async with self.sessio_factory() as session:
              yield session
              
db_helper = DatabaseHalper(
    url = "postgresql+asyncpg://postgres:password123@localhost:5433/vectordb",
    echo = False,
    echo_pool = False,
    pool_size = 5,
    max_overflow = 10

)



