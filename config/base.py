import logging


class BaseConfig:
    LOGGING_LEVEL = logging.INFO

    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://root:trantuandat26@localhost:3306/Gotit-final-project"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = "trantuandat"

    ITEMS_PER_PAGE = 20
