from .local import Config as _Config


class Config(_Config):
    TESTING = True

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:trantuandat26@localhost:3306/test"
