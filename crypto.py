import pyDes

def encrypt_p2p(message,key1,key2,key3):
    triple_des_obj=pyDes.triple_des(key1+key2+key3,padmode=pyDes.PAD_PKCS5)
    encrypted_data=triple_des_obj.encrypt(message)
    return encrypted_data

def decrypt_p2p(encrypted_message,key1,key2,key3):
    triple_des_obj=pyDes.triple_des(key1+key2+key3,padmode=pyDes.PAD_PKCS5)
    decrypted_data=triple_des_obj.encrypt(encrypted_message)
    return decrypted_data

def decrypt_group_message(encrypted_message,key):
    pass