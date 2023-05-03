import random
import math


def is_prime(n):
  if n % 2 == 0:
    return n == 2
  d = 3
  while d * d <= n and n % d != 0:
    d += 2
  return d * d > n


def prime_number_p_or_q(length_bit):
  while True:
    number1 = random.getrandbits(length_bit)

    if is_prime(number1):
      return number1


def ellerF(p, q):
  return (p - 1) * (q - 1)


def public_key(p, q):
  f_eller =  ellerF(p, q)
  print("f_eller: ", f_eller)

  if (f_eller < 2):
    return "Not possible to find e"

  e = f_eller
  while e > 0:
    if is_prime(e):
      if (math.gcd(f_eller, e) == 1):
        return (e, p * q)
    e -= 1


def factorization(n):
  print("waiting factorisation: " , n ," . . .")
  new_n = int(n / 2)
  integerList = list(range(2, new_n))

  for i in range(new_n - 2):
    if is_prime(integerList[i]):
      p = integerList[i]
      if (n % integerList[i] == 0):
        q = int(n / integerList[i] )
        if is_prime(q):
          return (p, q)


def private_key(public_key):
  e = public_key[0]
  n = public_key[1]
  d_test = False

  p, q = factorization(n)

  print(p, q)
  phi_n = ellerF(p, q)

  verification_number = phi_n + 1

  d = verification_number / e
  while d < phi_n:
    if(verification_number % e == 0):
      d_test = True
      break
    verification_number += phi_n
    d = verification_number / e
  
  if (d_test):
    return(int(d), n)
  else:
    return "не возможно посчитать d"

  
# k = 8, 2^(k/2) = 2^(8/2) = 2^4 = 16.
def main_f(length_bit):
  p = prime_number_p_or_q(length_bit // 2)
  q = prime_number_p_or_q(length_bit // 2)
  n =  p * q
  print (p, q, n)

  pub_k = public_key(p, q)
  if (isinstance(pub_k, tuple)):
    priv_k = private_key(pub_k)
    return pub_k, priv_k
  else:
    return "не удалось найти ключ private_key, public_key:" + pub_k
  
def fast_power(c, d, n):
  result = 1
  while d > 0:
    if d % 2 == 1:
      result = (result * c) % n
    c = (c * c) % n
    d //= 2
  return result
  
# 23 * 38 % 97 == 1 // exemple: pow(38, -1, mod=97)
def encrypt(m, pub_k): 
  e, n = pub_k
  print("encrypt e: ", e, " n: " , n, " m: ", m)
  return fast_power(m, e, n)

def decrypt(c, priv_k):
  d, n = priv_k
  print("decrypt d: ", d, "n" , n, " c: ", c)
  return fast_power(c, d, n)


message0 = [9197, 6284, 12836]
message = [9197, 6284, 12836, 8709, 4584, 10239, 11553, 4584, 7008, 12523, 9862, 356, 5356, 1159, 10280, 12523, 7506, 6311]
message2 = [671828605, 407505023, 288441355, 679172842, 180261802]


def testMessageDecrypt(message, pub_k):
  print("****************************************")

  priv_k = private_key(pub_k)
  print(f'Public key: {pub_k}')
  print(f'Privat key: {priv_k}')

  if type(message) == list:
    for element in message:
      print("----------------------------------------")
      print("chiffre: ", element)
      print("decrypt: ", decrypt(element, priv_k))
  else:
    print("----------------------------------------")
    print("chiffre: ", message)
    print("decrypt: ", decrypt(message, priv_k))
  print("****************************************")


def testMessageEncrypt(message, pub_k):
  print("****************************************")
  priv_k = private_key(pub_k)
  print(f'Public key: {pub_k}')
  print(f'Privat key: {priv_k}')

  if type(message) == list:
    for element in message:
      print("----------------------------------------")
      print("message: ", element)
      print("encrypt: ", encrypt(element, pub_k))
  else:
    print("----------------------------------------")
    print("message: ", message)
    print("encrypt: ", encrypt(message, pub_k))
  print("****************************************")


def testMessageEncryptAndtDecrypt(message, pub_k):
  print("******************************************")
  priv_k = private_key(pub_k)
  print(f'Public key: {pub_k}')
  print(f'Privat key: {priv_k}')

  if type(message) == list:
    for element in message:
      print("----------------------------------------")
      print("message: ", element)
      chiffre = encrypt(element, pub_k)
      print("chiffre: ", chiffre)
      print("decrypt: ", decrypt(chiffre, priv_k))
  else:
    print("----------------------------------------")
    print("message: ", message)
    chiffre = encrypt(message, pub_k)
    print("chiffre: ", chiffre)
    print("decrypt: ", decrypt(chiffre, priv_k))
  print("****************************************")



# ---------------------------------------

# (1.a)

# pub_k, priv_k = main_f(14)

# print("Public key:", pub_k)
# print("Privat key:", priv_k)

# ---------------------------------------

# (1.b)

# pub_k, priv_k = main_f(14)
# m = 14

# chiffre = encrypt(m, pub_k)
# message = decrypt(chiffre, priv_k)

# print("Public key:", pub_k)
# print("Privat key:", priv_k)
# print("Original message:", m)
# print("Encrypted message:", chiffre)
# print("Decrypted message:", message)


# ---------------------------------------

# (2.a)

# testMessageEncryptAndtDecrypt(message, (12413, 13289))

# ---------------------------------------

# (2.b)

# testMessageEncryptAndtDecrypt(message2, (163119273, 755918011))

# ---------------------------------------

# (3.a)

key_length = 14
public_key, private_key = main_f(key_length)
print("Public key:", public_key)
print("Privat key:", private_key)

# ---------------------------------------

# (3.b)
# (40^2 - 1) = 1599

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ_ .?€0123456789"
modulo_n = public_key[1]
block_size = 1
while (40 ** block_size) < modulo_n:
  block_size += 1
block_size -= 1
print("Size of block:", block_size)


# ---------------------------------------

# (3.c)

def text_to_numbers(text, alphabet):
  numbers = []
  for char in text:
    if char in alphabet:
        numbers.append(alphabet.index(char))
    else:
      print(char + " no in alphabet")
      return None
  return numbers


message = "HELLO WORLD"
encoded_message = text_to_numbers(message, alphabet)
print("Encoded message:", encoded_message)

# ---------------------------------------

# (3.d)
encrypted_message = [encrypt(number, public_key) for number in encoded_message]
print("Encrypted message:", encrypted_message)

# ---------------------------------------

# (3.e)
def numbers_to_text(numbers, alphabet):
  text = []
  for number in numbers:
    if 0 <= number < len(alphabet):
      char = alphabet[number]
      text.append(char)
    else:
      print(char + " no in alphabet")
  return ''.join(text)

def split_number(number, base):
  digits = []
  while number > 0:
    digits.append(number % base)
    number //= base
  return digits

def encrypted_numbers_to_text(encrypted_numbers, alphabet):
  base = len(alphabet)
  encrypted_blocks = [split_number(number, base) for number in encrypted_numbers]
  encrypted_text = ''.join(numbers_to_text(block, alphabet) for block in encrypted_blocks)
  return encrypted_text

encrypted_text = encrypted_numbers_to_text(encrypted_message, alphabet)
print("Encrypted text:", encrypted_text)

# ---------------------------------------

# (3.f)

decrypted_message = [decrypt(number, private_key) for number in encrypted_message]
print("Decrypted message:", decrypted_message)

decrypted_text = numbers_to_text(decrypted_message, alphabet)
print("Decrypted text:", decrypted_text)

# ---------------------------------------
