from base64 import b64encode

def fixed_length_xor(text, key):
    
    # XOR each byte of the text with the corresponding byte of the key
    xor_output = bytes([a ^ b for a, b in zip(text, key)])
    print(xor_output)
    
    return xor_output

# Laat deze asserts onaangetast!
assert type(fixed_length_xor(b'foo',b'bar')) == bytes
assert b64encode(fixed_length_xor(b'foo',b'bar')) == b'BA4d'

def repeating_key_xor(text, key):

# De sleutel wordt herhaaldelijk vermenigvuldigd totdat de lengte ervan gelijk is aan of groter is dan de lengte van de tekst.
# Dit wordt gedaan door de sleutel te vermenigvuldigen met de gehele deling van de lengte van de tekst door de lengte van de sleutel, plus één.
# Dit zorgt ervoor dat de sleutel minstens zo lang is als de tekst.
# Vervolgens wordt de sleutel gesneden tot de lengte van de tekst, waardoor deze precies even lang is als de tekst.
    key = (key * (len(text) // len(key) + 1))[:len(text)]
    print(key)

# De functie fixed_length_xor wordt vervolgens aangeroepen met de tekst en de sleutel.
# Deze functie voert een binaire XOR-operatie uit op de tekst en de sleutel, byte voor byte.
# Het resultaat van deze bewerking wordt opgeslagen in de variabele xor_output.
    xor_output = fixed_length_xor(text, key)
    print(xor_output)
    return xor_output

# Laat deze asserts onaangetast!
assert type(repeating_key_xor(b'all too many words',b'bar')) == bytes
assert b64encode(repeating_key_xor(b'all too many words',b'bar'))\
   == b'Aw0eQhUdDUEfAw8LQhYdEAUB'
