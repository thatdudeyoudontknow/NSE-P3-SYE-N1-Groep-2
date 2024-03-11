def string_to_b64(asciiString):
    """
    Converts a given ASCII-string to its b64-encoded equivalent.

    Parameters
    ----------
    asciiString : string
        string to be converted

    Returns
    -------
    bytes
        b64-encoded bytes-object representing the original string
    """

    return b64String

# Laat deze asserts onaangetast!
assert type(string_to_b64("foo")) == bytes
assert string_to_b64("Hello World") == b'SGVsbG8gV29ybGQ='

def b64_to_string(b64String):
    """
    Converts a given b64-string to its ASCII equivalent.

    Parameters
    ----------
    b64String : bytes
        b64-encoded bytesobject to be converted

    Returns
    -------
    string
        ASCII string
    """

    return asciiString

# Laat deze asserts onaangetast!
assert type(b64_to_string("SGVsbG8gV29ybGQ=")) == str
assert b64_to_string("SGVsbG8gV29ybGQ=") == "Hello World"