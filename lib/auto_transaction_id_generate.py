import random
import string

def generate_transaction_id():
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=7))