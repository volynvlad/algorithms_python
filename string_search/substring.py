import sys
import time


def knuth_morris_pratt(text, pattern):
    fail = _kmp_create_array(pattern)
    str_index = 0
    sub_index = 0
    occ = []
    while str_index < len(text):
        if text[str_index] == pattern[sub_index] \
                and sub_index == len(pattern) - 1:
            occ.append(str_index - len(pattern) + 1)
            str_index += 1
            sub_index = 0 if sub_index == 0 else fail[sub_index - 1]
        elif text[str_index] == pattern[sub_index]:
            str_index += 1
            sub_index += 1
        elif text[str_index] != pattern[sub_index] and sub_index == 0:
            str_index += 1
        else:
            sub_index = fail[sub_index - 1]
    return occ


def _kmp_create_array(pattern):
    fail = [0]
    i = 1
    j = 0
    while i < len(pattern):
        if pattern[i] == pattern[j]:
            fail.append(j + 1)
            i += 1
            j += 1
        elif pattern[i] != pattern[j] and j == 0:
            fail.append(0)
            i += 1
        else:
            j = fail[j - 1]
    return fail


def boyer_moore(text, pattern):
    shifts = _boyer_moore_create_shifts(pattern)

    i = 0
    text_len = len(text)
    pattern_len = len(pattern)
    occ = []
    while i <= text_len - pattern_len:
        num_of_skips = 0
        j = pattern_len - 1
        while j >= 0:
            if pattern[j] != text[i + j]:
                num_of_skips = max(1, j - (shifts[text[i + j]] if text[i + j] in shifts else -1))
                break
            j -= 1
        if num_of_skips == 0:
            occ.append(i)
            i += pattern_len
        i += num_of_skips
    return occ


def _boyer_moore_create_shifts(pattern):
    shift = {}
    for i, x in enumerate(pattern):
        shift[x] = i
    return shift


def rabin_karp(text, pattern):

    r = 53
    m = 997
    pattern_hash = 0
    current_substring_hash = 0
    degree = 1  # current power of r

    text_len = len(text)
    pattern_len = len(pattern)

    i = 0
    # h(s) = sum_0_n-1(s_i * r ** i) % m
    # calculate hash value for the pattern
    while i < pattern_len:
        pattern_hash += ord(pattern[i]) * degree
        pattern_hash %= m

        current_substring_hash += ord(text[text_len - pattern_len + i]) * degree
        current_substring_hash %= m

        if i != pattern_len - 1:
            degree = degree * r % m
        i += 1

    occ = []

    i = text_len
    while i >= pattern_len:
        if pattern_hash == current_substring_hash:
            is_pattern_found = True

            j = 0
            while j < pattern_len:
                if text[i - pattern_len + j] != pattern[j]:
                    is_pattern_found = False
                    break
                j += 1
            if is_pattern_found:
                occ.append(i - pattern_len)

        if i > pattern_len:
            current_substring_hash = (current_substring_hash - ord(text[i - 1]) * degree % m + m) * r % m
            current_substring_hash = (current_substring_hash + ord(text[i - pattern_len - 1])) % m

        i -= 1
    return occ


if __name__ == "__main__":
    def test(string_search):
        with open("book.txt") as f:
            pattern = "python" if len(sys.argv) < 2 else sys.argv[1]
            text = f.read().lower()
            start = time.time()
            array = string_search(text, pattern)
            end = time.time()
            start_index = -1 if len(array) == 0 else array[0]
            print(len(array))
            print(f"time = {end - start}")
            print(text[start_index: start_index + len(pattern)])
#             for index in array:
#                 print(index, text[index: index + len(pattern)])

    test(knuth_morris_pratt)
    print('-' * 20)
    test(boyer_moore)
    print('-' * 20)
    test(rabin_karp)
