def fix_word(word):
    """
    Recovers the words, fixing the letter outbreaks that occurrered

    In a pair of a uppercase letter followed by that same letter but lowercase, or the opposite, we remove both characters
    and repeat until that sort of outbreak doesn't happen anymore

    str --> str
    """

    for i in range(len(word) - 1):
        if (word[i].islower() and word[i + 1].isupper() and word[i].lower() == word[i + 1].lower()) or (word[i].isupper() and word[i + 1].islower() and word[i].upper() == word[i + 1].upper()): # verificar se vem upper/lower seguido do oposto e se a letter é a mesma
            word2 = word[:i] + word[i+2:]
    try: # if no changes are made to the word, word2 never gets definied and a NameError gets thrown, so a try/except is used to catch it 
        if word2 == word:
            return word2
        else:
            return fix_word(word2) # Since changes have been made, search for more recursively
    except NameError:
        return word # If no changes are made

def is_anagram(chain1, chain2):
    """
    Verifies if two words are anagrams of each other and returns True if so
    If the words are the same it also returns True

    str x str --> bool
    """

    if chain1.lower() == chain2.lower(): 
        return True
    if sorted(chain1.lower()) == sorted(chain2.lower()): # if all the characters are the same, then the chains sorted must be the same
        return True
    else:
        return False

def fix_doc(doc):
    """
    Applies the cuntions fix_word and is_anagra, to a string of characters that represents the text with the errors from
    the Buggy Data Base to fix the outbreaks and only leaving the first occurrence of an anagram

    Generates a ValueError if the given argument is invalid: the words can only be separated by a single white space, the
    text must have at least one word and each word has at least one letter.

    str --> str
    """

    try:
        if len(doc.split()) < 1:
            raise ValueError('fix_doc: invalid argument')
        for word in doc.split():
            if len(word) < 1:
                raise ValueError('fix_doc: invalid argument')
        for letter in doc:
            if not (letter.isalpha() or letter.isspace()) or '  ' in doc:
                raise ValueError('fix_doc: invalid argument')
        
        doc2 = ''
        for word in doc.split(): # split() to transform the string in a list where each word is an entry
            doc2 += fix_word(word) + ' '
        

        doc3 = doc2.split()

        to_remove = []

        for j in doc3:
            for k in doc3:
                if not k.lower() == j.lower():
                    if is_anagram(j, k): 
                        if doc3.index(j) < doc3.index(k): # checks which anagram occurs first
                            if k not in to_remove:
                                to_remove.append(k) 
                        elif j not in to_remove:
                                to_remove.append(j)

        for remove in to_remove:

            doc3.remove(remove)
        

        final = ''
        for word in doc3:
            final += word + ' '

        return final.rstrip() # remove the final white space at the end of the text
    except:
        raise ValueError('fix_doc: invalid argument')

moves = {1:{"R":2, "L": 1, "U":1, "D":4},2:{"R":3, "L": 1, "U":2, "D":5},3:{"R":3, "L": 2, "U":3, "D":6},4:{"R":5, "L": 4, "U":1, "D":7},5:{"R":6, "L": 4, "U":2, "D":8},6:{"R":6, "L": 5, "U":3, "D":9},7:{"R":8, "L": 7, "U":4, "D":7},8:{"R":9, "L": 7, "U":5, "D":8},9:{"R":9, "L": 8, "U":6, "D":9}}

def get_position(chain, integrer):
    """
    Receives a string with only one character that represents the direction of the movement and a number, which represents
    the current position

    Using a dictionary moves, returns the position after the move

    str x int --> int

    """
    return moves[integrer][chain]

def get_digit(seq, initial):
    """
    Receives a string with one or more characters and also a number, representing the initial position

    Using the same dictionary moves, returns the position after going through all moves

    str x int --> int
    """

    current = initial
    for move in seq:
        current = get_position(move, current)

    return current

def get_pin(tup):
    """
    Receives a tuple with 4 to 10 move sequences and returns a tuple with the correct PIN, according to those sequences

    It validates the given argument, where each element contains at least one character and it must be "U", "D", "L" or "R" 

    tuple --> tuple
    """

    if type(tup) != tuple:
        raise ValueError('get_pin: invalid argument')

    for element in tup:
        if type(element) != str:
            raise ValueError('get_pin: invalid argument')

        for letter in element:
            if letter not in ["U", "D", "L", "R"]:
                raise ValueError('get_pin: invalid argument')
    
    if not 4 <= len(tup) <= 10:
        raise ValueError('get_pin: invalid argument')

    for i in range(len(tup)):
        if len(tup[i]) < 1:
            raise ValueError('get_pin: invalid argument')
        if not tup[i].isalpha():
            raise ValueError('get_pin: invalid argument')


    values = []

    for i in range(len(tup)):
        if i == 0:
            current = get_digit(tup[i], 5) # assumes the initial position is the number 5
            
        else:
            current = get_digit(tup[i], current)
            
        values.append(current)
        
    return tuple(values)

def is_entry(arg):
    """
    Receives an argument of any type but only returns True if it corresponds to a BDB's entry (tuple with 3 fields,
    corresponding to a cipher, a control sequence and a security sequence)

    - Cipher contains one or more encrypted words, delimited by "-"
    - Control sequence is composed by 5 lowercase letters between "[ ]"
    - Security sequence is a tuple with two or more positive integrers

    universal --> bool
    """

    valid = False
    
    if type(arg) != tuple:
        return False

    if len(arg) != 3:
        return False

    if type(arg[0]) != str or type(arg[1]) != str or type(arg[2]) != tuple:
        return False

    if len(arg[0]) > 0 and len(arg[1]) == 7 and len(arg[2]) > 1:
        if not " " in arg[0]:
            if arg[0][0] != '-' and arg[0][-1] != '-':
                if arg[1][0] == '[' and arg[1][6] == ']' and arg[1].islower():
                    if arg[1].count('[') == 1 and arg[1].count(']') == 1:
                        if not '--' in arg[0]:
                            for c in arg[0]:
                                if c == '-' or (c.isalpha() and c.islower()):
                                    valid = True
                                else:
                                    valid = False

    if valid:
        for number in arg[2]:
            if not (type(number) == int and number > 0):
                valid = False
    
    return valid

def validate_cipher(cipher, control):
    """
    Receives two strings, one being a cipher and the other a control sequence
    it will return True only if both arguments are compatible
    
    str x str --> bool
    """

    valid = False
    letters = []
    numbers = []

    if is_entry((cipher, control, (950,300))): 
        for c in cipher:
            if c.isalpha and not c in letters and c != '-':
                letters.append(c)

        letters = sorted(letters) # alphabetic order

        for letter in letters:
            numbers.append(cipher.count(letter)) # how many times each letter is present

        dic = dict(zip(letters,numbers)) # dictionary with both lists

        sorted_dic = sorted(dic, key=dic.get, reverse=True)[:5] # sort letters by amount of times they appear, from most to less
        a = "".join(sorted_dic)
        if control[1:-1] == a:
            valid = True
        else:
            valid = False
    else:
        valid = False

    return valid

def filter_bdb(entries):
    """
    Receives a list with many BDB entries and using the previous functions, returns entries where the cipher
    and control sequences are not compatible with each other

    Also verifies the validity of the given argument, throwing a ValueError if it's invalid

    list --> list
    """
    
    if type(entries) != list:
        raise ValueError('filter_bdb: invalid argument')
    if len(entries) < 1:
        raise ValueError('filter_bdb: invalid argument')
    filtered = []
    for entry in entries:
        
        if not is_entry(entry):
            raise ValueError('filter_bdb: invalid argument')

        if not validate_cipher(entry[0], entry[1]):
            filtered.append(entry)
            
    return filtered          

def grab_security_number(tup):
    """
    Receives a tuple of positive integres and returns the lesser positive difference
    between any pair between them

    tuple --> integrer
    """

    difs = []
    for a in tup:
        for b in tup:
            if not id(a) == id(b):
                difference = a - b
                if difference < 0:
                    difference = - difference

                difs.append(difference)

    return min(difs)


def decipher_text(cif, seg):
    """
    Receives a string of characters that corresponds to a cipher and a security number
    Changes each letter of the cipher moving forward in the alphabet a number of times equal to the security number and, if the letter
    is on an even position, moves one more forward. If it's on a odd position, moves one backwards
    "-" transform into white spaces

    str x int --> str
    """

    abc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    lista = list(cif)
    for letter in range(len(lista)):
        if letter % 2 == 0:
            i = 1
        else:
            i = -1

        if lista[letter] == "-":
            lista[letter] = " "
        else:
            lista[letter] = abc[(abc.index(lista[letter]) + seg + i) % 26]
          
    return ("".join(lista))

def decipher_bdb(lista):
    """
    Recebe uma lista contento pelo menos uma entry da BDB e devolve uma lista do mesmo
    tamanho com as entries decipherdas de acordo com as funções anteriores.

    Verifica a validade do seu argumento, gerando um ValueError caso o mesmo não seja válido.
    
    lista --> lista
    """
    if type(lista) != list:
        raise ValueError('decipher_bdb: invalid argument')

    deciphered = []
    for entry in lista:
        if not is_entry(entry):
            raise ValueError('decipher_bdb: invalid argument')

        else:
            deciphered.append(decipher_text(entry[0], grab_security_number(entry[2])))

    return deciphered

def is_user(dic):
    """
    Receives an argument of any type and returns True only if that arguments corresponds to a
    dictionary with a name, password and individual rule, according to BDB's requisites

    Name and password must have more than one character

    universal --> bool
    """

    if type(dic) != dict:
        return False

    if len(dic) != 3:
        return False

    if not ("name" in dic.keys() and "pass" in dic.keys() and "rule" in dic.keys()):
        return False
    else:
        if not "rule" in dic.keys():
            return False
        else:
            if not ("vals" in dic["rule"].keys() and "char" in dic["rule"].keys()):
                return False

    if type(dic["rule"]) != dict or type(dic["rule"]["vals"]) != tuple or type(dic["rule"]["char"]) != str or type(dic["name"]) != str or type(dic["pass"]) != str:
        return False

    if len(dic["name"]) > 0 and len(dic["pass"]) > 0 and len(dic["rule"]["vals"]) == 2 and len(dic["rule"]["char"]) == 1:
        if dic["rule"]["vals"][0] < 1 or dic["rule"]["vals"][1] < 1:
            return False
        else:
            if dic["rule"]["vals"][1] < dic["rule"]["vals"][0]:
                return False
    else:
        return False

    return True

def is_valid_password(password, rule):
    """
    Receives a passowrd and a dictionary with an individual rule. Returns True only if the criteria is met

    Passwords must contain at least 3 lowercase vowels and at least one character appears twice in a row
    Rule is composed by two elements: vals and char. vals is a tuple with two positive integrers corresponding to the minimum and
    to the maximum amount of times that a letter (char) appears in the password.

    str x dict --> bool
    """
    present_vowels = 0
    passed_general, passed_individual = False, False

    ## -- global rules -- ##
    
    for letter in password: # -----
        if letter in ['a', 'e', 'i', 'o', 'u']:
            present_vowels += 1
    if present_vowels > 2: # valid password
        for i in range(len(password) - 1):
            if password[i] == password[i +1]: # check if has two consecutive letters that are equal
                passed_general = True              

    if passed_general:

        ## -- individual rules -- #
        
        number = password.count(rule["char"])
        if number >= rule["vals"][0] and number <= rule["vals"][1]:
            passed_individual = True

    if passed_general and passed_individual:
        return True
    else:
        return False

def filter_passwords(lista):
    """
    Receives a list with many BDB entries and filters the users with incorrect passwords, returning
    a list with them sorted alphabetically

    If the given argument is invalid, throws a ValueError

    list --> list
    """
    
    invalids = []
    if type(lista) != list:
        raise ValueError('filter_passwords: invalid argument')
    if len(lista) == 0:
        raise ValueError('filter_passwords: invalid argument')
    for entry in lista:
        if not is_user(entry):
            raise ValueError('filter_passwords: invalid argument')
        else:
            if not is_valid_password(entry["pass"], entry["rule"]):
                invalids.append(entry["name"])

    return sorted(invalids)