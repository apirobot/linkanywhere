from .local import Local


class Testing(Local):
    Local.INSTALLED_APPS += ('tests', )
