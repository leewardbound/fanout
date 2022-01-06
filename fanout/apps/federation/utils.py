from django.conf import settings


def is_local(url):
    if not url:
        return True

    d = settings.FEDERATION_HOSTNAME
    return url.startswith("http://{}/".format(d)) or url.startswith("https://{}/".format(d))
