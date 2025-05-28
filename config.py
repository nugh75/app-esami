import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'pef-esami-secret-key-2023'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///esami_pef.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurazioni per file upload (se necessario in futuro)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Configurazioni per sessioni
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Configurazioni per l'applicazione
    ITEMS_PER_PAGE = 20
    
class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False
    
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
