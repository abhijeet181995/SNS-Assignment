import pyDes
from Crypto.Cipher import AES           # Run `pip3 install pycryptodome` to install
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad

def encrypt_p2p(message,key1,key2,key3):
    triple_des_obj=pyDes.triple_des(key1+key2+key3,padmode=pyDes.PAD_PKCS5)
    encrypted_data=triple_des_obj.encrypt(message)
    return encrypted_data

def decrypt_p2p(encrypted_message,key1,key2,key3):
    triple_des_obj=pyDes.triple_des(key1+key2+key3,padmode=pyDes.PAD_PKCS5)
    decrypted_data=triple_des_obj.decrypt(encrypted_message)
    return decrypted_data

#message data-type is bytes and return is also bytes, key is in string
def encrypt_group_msg(message, key):
    hash_obj = SHA256.new(key.encode('utf-8'))    
    hkey = hash_obj.digest()
    cipher = AES.new(hkey, AES.MODE_ECB)
    result = cipher.encrypt(pad(message,16))
    return result  

#input and output both are in bytes, key is in string
def decrypt_group_message(encrypted_message, key):
    hash_obj = SHA256.new(key.encode('utf-8'))    
    hkey = hash_obj.digest()
    decipher = AES.new(hkey, AES.MODE_ECB)
    pt = decipher.decrypt(encrypted_message)
    decrypted_message=unpad(pt,16)
    return decrypted_message

# msg = "ASsdf"
# cipher_text = encrypt_group_msg(msg, "anything")
# print(cipher_text)

# plaintext = decrypt_group_message(cipher_text, "anything")
# print(plaintext)

