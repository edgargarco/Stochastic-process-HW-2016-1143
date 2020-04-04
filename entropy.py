import math as mt
import os
from collections import Counter
from operator import itemgetter

Shannon_Fano_dict = {}


def create_new_file(fname, message):
    try:
        file = open(fname, "w")
        file.write(message)
        file.close()
    except IOError:
        print("Something went wrong")


def reversed_bit_stream(bin_stream):
    bin_stream = bin_stream[2:]
    bin_stream = bin_stream[::-1]
    return bin_stream


def read_compressed_file(fname, length):
    try:
        with open(fname, 'rb') as f:
            bin_data = f.read()
            i = int.from_bytes(bin_data, byteorder='little')
            bin_number = bin(i)

        bin_stream = reversed_bit_stream(str(bin_number))
        len_bin_stream = len(bin_stream)

        if length != len_bin_stream:
            new_stream = ''
            aux = length - len_bin_stream
            new_stream = '0' * aux
            new_stream = bin_stream + new_stream

    except IOError:
        print("Something went wrong while reading file")


def create_compressed_file(fname, compresses_message):
    try:
        length = len(compresses_message)

        bin_data = int(compresses_message[::-1], 2).to_bytes(int(length // 8) + 1, 'little')
        file = open(fname, "wb")
        file.write(bin_data)
        file.close()
        return length
    except IOError:
        print("Something went wrong while writing file")


def file_read(fname):
    with open(fname, "r") as file:
        data = file.read().replace('\n', '')
        return data


def char_classification(data):
    char_dict = Counter(data)
    return char_dict


def char_amount(char_dict):
    return sum(char_dict.values())


def probability_calculation(char_dict, chart_amount):
    probability_dict = Counter({key: char_dict[key] / chart_amount for key in char_dict})
    return probability_dict


def shannon_entropy_H(probability_dict):
    entropy = 0
    for key in probability_dict:
        entropy = entropy + -1 * (probability_dict[key] * mt.log(probability_dict[key], 2))
    return entropy


def Shannon_Fano_coding(seq, code):
    a = {}
    b = {}
    if len(seq) == 1:
        Shannon_Fano_dict[seq.popitem()[0]] = code
        return 0
    for i in sorted(seq.items(), key=itemgetter(1), reverse=True):
        if sum(a.values()) < sum(b.values()):
            a[i[0]] = seq[i[0]]
        else:
            b[i[0]] = seq[i[0]]
    Shannon_Fano_coding(a, code + "0")
    Shannon_Fano_coding(b, code + "1")


def Shannon_Fanon_Average_length(Shannon_Fano_dict, probability_dict):
    if len(Shannon_Fano_dict) == len(probability_dict):
        average = 0
        for i in Shannon_Fano_dict:
            average = average + len(Shannon_Fano_dict[i]) * probability_dict[i]
        return average


def Shannon_Fano_print_dict(Shannon_Fano_dict):
    for i in sorted(Shannon_Fano_dict):
        print(i, "=", Shannon_Fano_dict[i])


def message_to_Fanon_Code(message, Shannon_Fano_dict):
    code_mes = ""
    for i in message:
        code_mes += Shannon_Fano_dict[i]
    # print("\nMessage length in code: ", len(code_mes), "\nMessage code: ", code_mes)
    return code_mes

txt_name = "el_quijote.txt"
message = file_read(txt_name)
var = char_classification(message)
probability = probability_calculation(var, char_amount(var))
print("Repetition of each character in file ",txt_name)
print(dict(var))

# Theory Entropy Calculation
print("\nEntropy == ", shannon_entropy_H(probability))

# Shannon Coding
Shannon_Fano_coding(dict(var), "")

# Shannon Dictionary of coded Dictionary
print("\nShannon Dictionary of coded Dictionary")
print(Shannon_Fano_dict)

print("\nDictionary of Probabilities")
print(dict(probability))

print("\nThe average length of the Shannon-Fano code is == ",
      Shannon_Fanon_Average_length(Shannon_Fano_dict, probability))

# message_to_Fanon_Code(message,Shannon_Fano_dict)
length = create_compressed_file("compressed", message_to_Fanon_Code(message, Shannon_Fano_dict))
read_compressed_file("compressed", length)
print('Size in Bytes of uncompressed file', os.path.getsize('el_quijote.txt'), "bytes", "Size in Mega Bytes ",
      os.path.getsize('el_quijote.txt') / 1000000, "Mb")
print('Size in Bytes of compressed file', os.path.getsize('compressed'), "bytes", "Size in Mega Bytes ",
      os.path.getsize('compressed') / 1000000, "Mb")
