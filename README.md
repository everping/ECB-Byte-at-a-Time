# ECB Byte at a Time
This is an implement of Byte at a Time Attack on block encryption algorithms use ECB mode.

In this model:

`Cipher = Encrypt (input + secret, key)`

Where:
- `Encrypt()` is the encryption function uses block ciphers with ECB Mode
- `Cipher` is result of encryption
- `Input` is value that users can control
- `Secret` and the key are secret values stored in the server

This attack allows to find secret

`server.py` is a vulnerable app, and `crypanalysis.py` is the exploit code. My attack current apply to the AES, DES and 3DES algorithms
