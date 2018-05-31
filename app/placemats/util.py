import os


def chunks(l, n):
    return [l[i:i + n] for i in range(0, len(l), n)]


def kwargs_from_environ(environ_to_kwarg):
    """
    Adds environment variables to a client kwargs dict that's used to
    configure the biopython ncbi client.
    :param environ_to_kwarg:
    """
    env_keys = filter(lambda k: k in os.environ, environ_to_kwarg.keys())
    return {environ_to_kwarg[k]: os.environ[k] for k in env_keys}
