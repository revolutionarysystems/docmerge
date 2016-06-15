try:
    from docmerge.config_custom import install_name, install_display_name, gdrive_root, local_root, email_credentials, email_default_recipient, remote_library, extend_path
except:
    from .config_default import install_name, install_display_name, gdrive_root, local_root, email_credentials, email_default_recipient, remote_library, extend_path

