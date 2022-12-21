import cryptolib
import ubinascii


secret = 'somesecret'
secret = secret + "X" * (32-len(secret))
print(secret)
crypto_key = cryptolib.aes(bytes(secret, 'utf-8'), 1)
password = "timewr50m"
password = password + " "*(16 - len(password)%16)
print("'"+password+"'")
print(type(crypto_key.encrypt(password)))
encr = ubinascii.b2a_base64(crypto_key.encrypt(password))
print(encr.decode())
print(type(bytes(encr)))
print('-----')
crypto_key = cryptolib.aes(bytes(secret, 'utf-8'), 1)
print(type(bytes(encr)))
decr = crypto_key.decrypt(ubinascii.a2b_base64(encr)).decode()

print(decr.strip())