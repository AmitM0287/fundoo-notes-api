from fundoo_notes_app.settings import *


# Database

DATABASES = {
    'default': {
        'ENGINE': config.get('DB_ENGINE'),
        'NAME': config.get('TEST_DB_NAME'),
        'USER': config.get('DB_USER'),
        'PASSWORD': config.get('DB_PASSWORD'),
        'HOST': config.get('DB_HOST'),
        'PORT': config.get('DB_PORT'),
    }
}
