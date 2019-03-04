### This sample code includes most zymbit API 

import zymkey
from textwrap import fill

print('Testing data lock...')
src = bytearray(b'\x01\x02\x03\x04')
dst = zymkey.client.lock(src)
print('Original Data')
s = fill(' '.join('{:02X}'.format(c) for c in src), 49)
print(s)
print('Encrypted Data')
s = fill(' '.join('{:02X}'.format(c) for c in dst), 49)
print(s)
print('Testing data unlock...')
new_src = dst
new_dst = zymkey.client.unlock(new_src)
print('Decryped Data')
s = fill(' '.join('{:02X}'.format(c) for c in new_dst), 49)
print(s)

print('Turning LED on...')
zymkey.client.led_on()

print('Testing get_random() with 512 bytes...')
num = 512
random_bytes = zymkey.client.get_random(num)
s = fill(' '.join('{:02X}'.format(c) for c in random_bytes), 49)
print(s)

print('Turning LED off...')
zymkey.client.led_off()

print('Flashing LED off, 500ms on, 100ms off...')
zymkey.client.led_flash(500, 100)

print('Testing zkCreateRandDataFile with 1MB...')
num = 1024 * 1024
file_path = '/tmp/r.bin'
zymkey.client.create_random_file(file_path, num)

print('Turning LED off...')
zymkey.client.led_off()

print('Testing get_ecdsa_public_key()...')
pk = zymkey.client.get_ecdsa_public_key()
s = fill(' '.join('{:02X}'.format(c) for c in pk), 49)
print(s)

print('Testing create_ecdsa_public_key_file()...')
zymkey.client.create_ecdsa_public_key_file('/tmp/pk.pem')


