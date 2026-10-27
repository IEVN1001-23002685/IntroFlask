class DevelopmentConfig:
    DEBUG = True
    MYSQL_HOST = "mysql"
    MYSQL_PORT = 3306
    MYSQL_USER = "saul"
    MYSQL_PASSWORD = "rootsaul"
    MYSQL_DB = "api_utl"
    MYSQL_CURSORCLASS = "Cursor"

config = {
    "development": DevelopmentConfig
}
