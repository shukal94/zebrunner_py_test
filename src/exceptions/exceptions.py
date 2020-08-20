class ProjectException(Exception):
    """ Common base exception for application """


class PageNotLoadedException(ProjectException):
    """ Expected page is not loaded """


class UIException(ProjectException):
    """ Basic exception, when some essential action not happened, so execution_tools can be stopped.
     Normally there is no sense to catch this exception  """


class ConfigException(ProjectException):
    """ testing framework configuration issues"""


class APIException(ProjectException):
    """ API call issue"""
