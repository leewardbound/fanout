import re
import unicodedata

from django.conf import settings


def is_local(url):
    if not url:
        return True

    d = settings.FEDERATION_HOSTNAME
    return url.startswith("http://{}/".format(d)) or url.startswith("https://{}/".format(d))


def slugify_username(username):
    """
    Given a username such as "hello M. world", returns a username
    suitable for federation purpose (hello_M_world).

    Preserves the original case.

    Code is borrowed from django's slugify function.
    """

    value = str(username)
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^\w\s-]", "", value).strip()
    return re.sub(r"[-\s]+", "_", value)
