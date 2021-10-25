import os
from django.core.exceptions import ImproperlyConfigured

def get_env_value(env_variable):
    try:
        return os.environ[env_variable]
    except KeyError:
        error_msg = f'Environment variable "{env_variable}" not set.'
        raise ImproperlyConfigured(error_msg)
