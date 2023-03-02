class Config:
    SECRET_KEY = 'thisisasecretkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True