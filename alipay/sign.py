# --*-- coding: utf-8 --*--
import base64
import hashlib
import os
import random

from Crypto.Hash import SHA
from Crypto.PublicKey import RSA, DSA
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5

from alipay import conf


def sign(data, encoding=None, sign_type=conf.sign_type, key_specs=[], exception_keys=['sign', 'sign_type']):
    req_keys = sorted([key for key in key_specs if key not in exception_keys])
    params = [(k, data[k]) for k in req_keys if k in data]
    query_string = '&'.join(['{}={}'.format(k, v) for (k, v) in params])
    query_string = query_string.encode(encoding) if isinstance(query_string, unicode) and encoding else query_string
    print 'signing_params'.center(40, '-')
    for k in req_keys:
        if k in data:
            print k, ':', data.get(k)
    print 'signing_string'.center(40, '-')
    print type(query_string), query_string
    return calc_sign(query_string, sign_type)


def calc_sign(query_string, sign_type=conf.sign_type):
    if sign_type.upper() == 'MD5':
        m = hashlib.md5()
        m.update(''.join([query_string, conf.md5_secret]))
        return m.hexdigest()
    if sign_type.upper() == 'RSA':
        with open(os.path.join(conf.crypto_root, 'r')) as f:
            key = f.read()
            rsa_key = RSA.importKey(key)
            signer = Signature_pkcs1_v1_5.new(rsa_key)
            digest = SHA.new()
            digest.update(query_string)
            signed = signer.sign(digest)
        return base64.b64encode(signed)
    if sign_type.upper() == 'DSA':
        key = import_dsa_key_from_file(os.path.join(conf.crypto_root, ''))
        h = SHA.new(query_string).digest()
        k = random.StrongRandom().randint(1, )
        signed = key.sign(h, k)
        return base64.b64encode(signed)


def import_dsa_key_from_file(file_name, encoding='base64'):
    from Crypto.Util import asn1
    with open(file_name) as f:
        seq = asn1.DerSequence()
        data = '\n'.join(f.read().strip().split('\n')[1:-1].decode(encoding))
        seq.decode(data)
        p, q, g, y, x = seq[1:]
        key = DSA.construct((y, g, p, q, x))
        return key


def export_dsa_key_to_file(file_name, key, encoding='base64'):
    from Crypto.Util import asn1
    with open(file_name) as f:
        seq = asn1.DerSequence()
        seq[:] = [0, key.p, key.q, key.g, key.y, key.x]
        template = '-----BEGIN DSA PRIVATE KEY-----\n%s-----END DSA PRIVATE KEY-----'
        exported_key = template % seq.encode().encode(encoding)
        f.write(exported_key)
