class Config: 
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres_user:postgres_pw@192.168.178.52:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    JWT_SECRET_KEY ='super_duper_secret'
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT=300             #globales Caching --> Aktualisierung des Cache alle 300 Sekunden
