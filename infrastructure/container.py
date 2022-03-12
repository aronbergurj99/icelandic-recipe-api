from dependency_injector import containers, providers
from infrastructure.settings import Settings

from db_connections.mongo_db_connection import MongoDbConnection
from auth.auth_handler import AuthHandler


class Container(containers.DeclarativeContainer):
    config: Settings = providers.Configuration()
    config.from_pydantic(Settings('./infrastructure/.env'))

    __db_connection_provider = providers.Selector(
        config.environment.value,
        dev = config.dev_mongo_db_connection
    )

    mongo_db_connection_provider = providers.Singleton(
        MongoDbConnection,
        uri=__db_connection_provider,
        db=config.database
    )

    auth_provider = providers.Singleton(
        AuthHandler,
        secret=config.secret,
        algorithm=config.algorithm
    )



