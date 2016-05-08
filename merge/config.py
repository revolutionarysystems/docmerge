try:
    from .config_custom import install_name, install_display_name, email_credentials, email_default_recipient, remote_library
except:
    from .config_default import install_name, install_display_name, email_credentials, email_default_recipient, remote_library

