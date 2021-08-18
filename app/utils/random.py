import random

number = "0123456789"
str_lowercase = 'abcdefghijklmnopqrstuvwxyz'
str_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
str_case = str_lowercase + str_uppercase
verification_code = number + str_case
str_character = '{%#)^;,(<+@!:}]",*''{|~$&.?-/,\\ =[_`>}'
string = str_case + str_character
password = number + string


def random_content(length=16, random_type='number'):
    if random_type == 'number':
        return ''.join(random.choice(number) for i in range(length))
    elif random_type == 'str_case':
        return ''.join(random.choice(str_case) for i in range(length))
    elif random_type == 'verification_code':
        return ''.join(random.choice(verification_code) for i in range(length))
    elif random_type == 'string':
        return ''.join(random.choice(string) for i in range(length))
    elif random_type == 'password':
        return ''.join(random.choice(password) for i in range(length))
    else:
        pwd = ''
        for i in range(length):
            pwd.join(random.sample(password, random.randint(2, 7)))
        return pwd
