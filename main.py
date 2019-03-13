import hashlib
import getpass
import requests

print('-----------------------------------------------------------------------------------------')
print('Hi there! We will check whether your password has been pwned using haveibeenpwned.com API')
print('Don\'t worry, we won\'t store or send your plaintext password anywhere!')
print('Rather we will send the first 5 character sha-1 hash of it and compare '
      'the remaining\npart with results obtained')
print('-----------------------------------------------------------------------------------------')
password = getpass.getpass('insert password: ')
hashed_pass = hashlib.sha1(password.encode('utf-8'))
hash_str = hashed_pass.hexdigest()
first, last = hash_str[:5].upper(), hash_str[5:].upper()
url = 'https://api.pwnedpasswords.com/range/{}'.format(first)
r = requests.get(url)

if r.status_code == 200:
    content = r.content.decode('utf-8')
    hashes_list = content.splitlines()
    _dict = {}
    for _hash in hashes_list:
        split_list = _hash.split(':', 1)
        _dict[split_list[0]] = split_list[1]
    if last in _dict:
        print('Bad news.. your password has been found {} times'.format(_dict[last]))
    else:
        print('Yeah! Seems like your password has never been pwned!')
else:
    print('Something wrong happened with haveibeenpwned.com API')
    print('Response status code:', r.status_code)
    print('Response headers:', r.headers)
