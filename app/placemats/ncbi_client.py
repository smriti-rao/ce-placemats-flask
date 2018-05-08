import Bio.Entrez

API_KEY = None


def configure_client(email='A.N.Other@example.com', api_key=None):
    """
    Must be called once before calling any of the other API's
    :param email:
    :param api_key:
    """
    Bio.Entrez.email = email
    global API_KEY
    API_KEY = api_key


def call(procedure, *args, **kwargs):
    """
    Wraps all our calls to Entrez api's. Acts as our 'http interceptor'.
    :param procedure: Entrez function to invoke
    :param args:
    :param kwargs:
    :return:
    """
    if API_KEY:
        kwargs['api_key'] = API_KEY
    handle = procedure(*args, **kwargs)
    output = Bio.Entrez.read(handle)
    handle.close()
    return output


def efetch(*args, **kwargs):
    """

    :param args:
    :param kwargs:
    """
    return call(Bio.Entrez.efetch, *args, **kwargs)


def egquery(*args, **kwargs):
    """

    :param args:
    :param kwargs:
    """
    return call(Bio.Entrez.egquery, *args, **kwargs)


def esearch(*args, **kwargs):
    """

    :param args:
    :param kwargs:
    :return:
    """
    return call(Bio.Entrez.esearch, *args, **kwargs)
