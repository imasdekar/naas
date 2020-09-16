from escapism import escape
from base64 import b64encode
import string

_docker_safe_chars = set(string.ascii_letters + string.digits)
_docker_escape_char_kubernet = "-"
_docker_escape_char_docker = "_"

def escape_kubernet(s):
    """Escape a string to kubernet-safe characters"""
    return escape(
        s,
        safe=_docker_safe_chars,
        escape_char=_docker_escape_char_kubernet,
    )
    
def escape_docker(s):
    """Escape a string to docker-safe characters"""
    return escape(
        s,
        safe=_docker_safe_chars,
        escape_char=_docker_escape_char_docker,
    )

def encode_proxy_url(token=''):
    client = os.environ.get('JUPYTERHUB_USER', '')
    base_public_url = os.environ.get('PUBLIC_PROXY_API', '')
    clientEncoded = escape_kubernet(client)
    message_bytes = clientEncoded.encode('ascii')
    base64_bytes = b64encode(message_bytes)
    username_base64 = base64_bytes.decode('ascii')
    return f"{base_public_url}/{username_base64}/{token}"
