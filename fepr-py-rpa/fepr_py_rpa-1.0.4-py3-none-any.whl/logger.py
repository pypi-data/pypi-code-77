from logging import config, getLogger, DEBUG, INFO

config.dictConfig({
    'version': 1,
    'formatters': {
        'defaltFormatter': {
            'format': '[%(asctime)s] [%(levelname)s] [%(funcName)s] : %(message)s'
        }
    },
    'handlers': {
        'consoleHandler': {
            'class': 'logging.StreamHandler',
            'formatter': 'defaltFormatter',
            'level': INFO
        }
    },
    'root': {
        'handlers': ['consoleHandler'],
        'level': INFO
    },
    'loggers': {
        'defalt': {
            'handlers': ['consoleHandler'],
            'level': INFO,
            'propagate': 0
        }
    }
})

logger = getLogger('defalt')

