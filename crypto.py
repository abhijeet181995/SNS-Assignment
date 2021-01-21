import pyDes
from Crypto.Cipher import AES           # Run `pip3 install pycryptodome` to install
from Crypto.Hash import SHA256

def encrypt_p2p(message,key1,key2,key3):
    triple_des_obj=pyDes.triple_des(key1+key2+key3,padmode=pyDes.PAD_PKCS5)
    encrypted_data=triple_des_obj.encrypt(message)
    return encrypted_data

def decrypt_p2p(encrypted_message,key1,key2,key3):
    triple_des_obj=pyDes.triple_des(key1+key2+key3,padmode=pyDes.PAD_PKCS5)
    decrypted_data=triple_des_obj.decrypt(encrypted_message)
    return decrypted_data

def encrypt_group_msg(message, key):
    hash_obj = SHA256.new(key.encode('utf-8'))    
    hkey = hash_obj.digest()
    msg = message
    BLOCK_SIZE = 16
    PAD = "{"
    padding = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PAD
    cipher = AES.new(hkey, AES.MODE_ECB)
    result = cipher.encrypt(padding(msg).encode('utf-8'))
    return result  

def decrypt_group_message(encrypted_message, key):
    hash_obj = SHA256.new(key.encode('utf-8'))    
    hkey = hash_obj.digest()
    msg = encrypted_message
    PAD = "{"
    decipher = AES.new(hkey, AES.MODE_ECB)
    pt = decipher.decrypt(msg).decode('utf-8')
    pad_index = pt.find(PAD)
    result = pt[: pad_index]
    return result

# msg = "ASsdf"
# cipher_text = encrypt_group_msg(msg, "anything")
# print(cipher_text)

# plaintext = decrypt_group_message(cipher_text, "anything")
# print(plaintext)

