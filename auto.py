#!/usr/bin/env python

import sys
import enchant

# The English library to validate words
d = enchant.Dict("en_US")

# The minimum length of the crib word
MIN_CRIB_LEN = 5

# The minimun length of the internal partial matching word
# This should be less or equal to MIN_CRIB_LEN
MIN_INTERNAL_LEN = 5

# Whether or not to pad the crib word with spaces on the left and right. 
# This allows you to get "free additional characters" for most words. Also
# lets you use shorter crib words.
PAD_SPACES = True

# Allowed non-alpha numeric characters
ALLOWED_PUNCTUATION=".?!\'\"( )"

# Load 10,000 most common english vocabulary words as crib word candidates
# Source: https://github.com/first20hours/google-10000-english
with open('google_words', 'rb') as f:
    crib_list = f.readlines()
crib_list = [x.strip() for x in crib_list] 

# This function is credit to https://github.com/SpiderLabs/cribdrag
# @param: 	ctext	- 	The cipher text to be crib dragged
# @param: 	crib 	- 	The crib word to drag on the cipher text
# @return: 	results - 	A list of result that generated from a or partial match
#						of the crib word on the cipher text. Each result is
#						ensured to be an English word and contain letters only
def sxor(ctext, crib):
    results = []
    single_result = ''
    crib_len = len(crib)
    positions = len(ctext)-crib_len+1
    for index in xrange(positions):
        single_result = ''
        for a,b in zip(ctext[index:index+crib_len],crib):
            single_result += chr(ord(a) ^ ord(b))

        # Check the word partially, to see whether it conatins an English word
        result_length = len(single_result)
        if (result_length >= MIN_INTERNAL_LEN and all(x.isalpha() or x.isdigit() or x in ALLOWED_PUNCTUATION for x in single_result)):
            for i in xrange(0, result_length - MIN_INTERNAL_LEN):
                for j in xrange(i + MIN_INTERNAL_LEN, result_length):
                    result_partial = single_result[i:j]
                    if (result_partial.isalpha()):
                        if (d.check(result_partial)):
                            results.append("\"" + single_result + "\" " + result_partial + "(" + str(index) + ")")

        # Check the whole word, to see whether it is an English word
        if (single_result.isalpha()):
            if(d.check(single_result)):
                results.append(single_result + "(" + str(index) + ")")
        
    return results

# This function executes the crib dragging of a single word on the cipher text
# And write/append the result to the target output file
def writeResultGivenCrib(ctext, crib):
    results = sxor(ctext, crib)
    results_len = len(results)
    # Write to the output (Append)
    with open(FILE_NAME, "a") as text_file:
        if (results_len > 0):
            text_file.write(crib + "(" + str(results_len) + "): [ " + ', '.join(results) + " ]\n")

# Provide the Hexidecimal version of cipher_text here
CIPHER_HEX = "1b1b522d0b04451a031652425e5e4e12595e1761413e0d0a492604080c4d002a001b0a0b0b5e003d0104011c003f081f45154115060b1d594e29100849011b4139411548051c01090024100000010300475718535a5e524c474440434e57001d444f00450b0a151f04540f1d014d420d1d0445150153081a0d4f0f4d1807131b54541c0d456928160c044e732c0f021e0d52364534191c0d01415c202c3d0500220645221c01171152221f181f434e314548151a4541390d4b261f0c171a0000161d1a180d0f170c434e490f4e2652060001161a536906050d415e523b11070a0b0307120016131b180a01411b41005504180a52070a0a000d1f00034f170445060f1c4d273d6a00150601001117134f5423190d4e633d020f0a1c0700201a5204010345461f521b0545416621060a543006101d4d030f190818104f01466c0406170d1b044e1d1d00071d021c0009410241110d0c014e42000045104f490f4c180712003a0d1148151d1f1207061a4c081a1d000f01114c010c004477084b0b0c170b070454684f211b16081a0e481d"
# Decode the hexidecimal cipher text
cipher_text = CIPHER_HEX.decode('hex')
# File Name
FILE_NAME = "auto_output.txt"

# Clear the content of the output file before starting to append
open(FILE_NAME, 'w').close()

# Iterate through the crib word list
for ind, crib in enumerate(crib_list):
    # Get the column of the word
    crib_word = " " + crib + " " if PAD_SPACES else crib

    # Write the result to the file
    if (len(crib_word) >= MIN_CRIB_LEN):
        writeResultGivenCrib(cipher_text, crib_word)
