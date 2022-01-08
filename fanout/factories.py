

class NoUpdateOnCreate:
    """
    Factory boy calls save after the initial create. In most case, this
    is not needed, so we disable this behaviour
    """

    @classmethod
    def _after_postgeneration(cls, instance, create, results=None):
        return
