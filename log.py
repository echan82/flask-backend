# log.py
import logging.config

LOG_CONFIG = {
    'version': 1,
    'filters': {
        'request_id': {
            '()': 'util.request_id.RequestIdFilter',
        },
    },
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s.%(module)s.%(funcName)s:%(lineno)d - %(levelname)s - %(request_id)s - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'filters': ['request_id'],
            'formatter': 'standard'
        },
        'timedRotatingFileHandler': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'DEBUG',
            'filename':'application.log',
            'filters': ['request_id'],
            'formatter': 'standard',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 0,
            'encoding': 'utf8'
        }

    },
    'loggers': {
        '': {
            'handlers': ['console','timedRotatingFileHandler'],
            'level':'DEBUG',
        },
        'app': {
            'handlers': ['console'],
            'level':'DEBUG',
        },
    }
}

logging.config.dictConfig(LOG_CONFIG)