from   .sendmail import GmailClient
import json


def load_config(path):
    with open(path, 'r') as f:
        config = json.load(f)

    email_config_path = config.pop("email_config")
    with open(email_config_path, 'r') as f:
        email_config = json.load(f)

    config['email_client'] = GmailClient(
        email_config['email_addr'], email_config['password']
    )

    return config
