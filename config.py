#!/usr/bin/python3

import hashlib
import binascii
import sys

# You can add all kind of config values to this file, e.g. CSV separator and file path
PATH = "/home/ckpeir/cgi-data/scores.csv"
SEP = ","
MAX = 10

# this dictionary contains users, which are allowed to add new high score values
# Key: user name, Value: password in hashed format
users = {
    "sovellus": "67c75b218d9355780f46f9dbada8bfefeeef92d047e1ee9a1024b648838b76a3d53e9da878bd0c735314c1d5940165cff8538868560b65cbd6284608a99fd34cbaf60163ab6d1d41cc521309955c293381d49cc41afd134fbc0ad93b20da031c",
    "testi": "689fcfdf0d227e6cadc386bfc8dc4411a26f1cf16ed33d9cb93b6758c1b63b9eb5476b5fa97e6be321dbe062684c21ab6e784f43831332aed4576698d0f57a3d9eaa19036276ca818c83caef21ac98049799cb9ea3b889c91ed4bce132e8e7f6"
}


def verify_password(user, provided_password):
  # use the global users variable
  global users
  # Verify a stored password against one provided by user
  if user not in users:
    return False

  stored_password = users[user]
  salt = stored_password[:64]
  stored_password = stored_password[64:]
  pwdhash = hashlib.pbkdf2_hmac('sha512',
                                provided_password.encode('utf-8'),
                                salt.encode('ascii'),
                                100000)
  pwdhash = binascii.hexlify(pwdhash).decode('ascii')
  return pwdhash == stored_password


def main():
  if len(sys.argv) != 3:
    print("Invalid arguments!")
    sys.exit(3)

  user = sys.argv[1]
  password = sys.argv[2]
  isValid = verify_password(user, password)
  if isValid:
    print("Oikea salasana")
  else:
    print("Väärä käyttäjätunnus ja/tai salasana!")


if __name__ == '__main__':
  main()
