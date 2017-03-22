import math
import hashlib

ALPHABET = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def get_alpha_ID(idnum, to_num=False, pad_up=False, passkey=None):
  index = ALPHABET
  if passkey:
    i = list(index)
    passhash = hashlib.sha256(passkey).hexdigest()
    passhash = hashlib.sha512(passkey).hexdigest() if len(passhash) < len(index) else passhash
    p = list(passhash)[0:len(index)]
    index = ''.join(zip(*sorted(zip(p,i)))[1])

  base = len(index)

  if to_num:
    idnum = idnum[::-1]
    out = 0
    length = len(idnum) -1
    t = 0
    while True:
      bcpow = int(pow(base, length - t))
      out = out + index.index(idnum[t:t+1]) * bcpow
      t += 1
      if t > length: break

    if pad_up:
      pad_up -= 1
      if pad_up > 0:
        out -= int(pow(base, pad_up))
  else:
    if pad_up:
      pad_up -= 1
      if pad_up > 0:
        idnum += int(pow(base, pad_up))

    out = []
    t = int(math.log(idnum, base))
    while True:
      bcp = int(pow(base, t))
      a = int(idnum / bcp) % base
      out.append(index[a:a+1])
      idnum = idnum - (a * bcp)
      t -= 1
      if t < 0: break

    out = ''.join(out[::-1])

  return out
