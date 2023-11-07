import sys


ACCOUNT_ENDPOINT = 'http://127.0.0.1:8001'
CREATE_OTP_ENDPOINT = 'http://127.0.0.1:8004/create_otp'
VERIFY_OTP_ENDPOINT = 'http://127.0.0.1:8004/verify_otp'


JWT_SECRET_KEY = '693364d5ccaf48dd5ad582fef7bd190591401694551819386b62ee9bd41ccf01'
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"

logging_config = {
    "version": 1,
    "formatters": {
        "custom-json": {
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(process)s %(levelname)s %(name)s %(module)s %(funcName)s %(lineno)s"
        }
    },
    "handlers": {
        "elastic-search": {
            "level": "INFO",
            "class": "app.log.elastic_handler.ElasticHandler",
            "formatter": "custom-json",
        },
    },
    "loggers": {
        "elastic-logger": {
            "level": "INFO",
            "handlers": ["elastic-search"],
            "propagate": True
        },
    },
}
