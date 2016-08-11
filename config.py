import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgres://esounbmxbkhyhz:YOSOeNqwN017-wqsEEkS2dTswk@ec2-50-19-223-15.compute-1.amazonaws.com:5432/d518d9048mrvj6'

# Might add more configs later
config = {
    'development': DevelopmentConfig,

    'default': DevelopmentConfig
}
