#!/usr/bin/env python
# -*- coding: utf-8 -*-
# quickslipper.py: Quicksilver-like string scoring.
# Copyright (C) 2010 Gora Khargosh <gora.khargosh@gmail.com>
# Copyright (C) 2009 Joshaven Potter <yourtech@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

def first_valid_index(a, b):
    minimum = min(a, b)
    if minimum > -1:
        return minimum
    return max(a, b)

def score(s, abbr):
    """

    Doctests:
    >>> assert score("hello world", "ax1") == 0
    >>> assert score("hello world", "ow") > 0.14
    >>> assert score("hello world", "h") >= 0.09
    >>> assert score("hello world", "he") >= 0.18
    >>> assert score("hello world", "hel") >= 0.27
    >>> assert score("hello world", "hell") >= 0.36
    >>> assert score("hello world", "hello") >= 0.45

    # assert score("hello world", "helloworld") >= 0.9
    # assert score("hello world", "hello worl") >= 0.9
    >>> assert score("hello world", "hello world") == 1

    >>> assert score("Hello", "h") >= 0.13
    >>> assert score("He", "h") > 0.35

    # Same case matches better than wrong case.
    >>> assert score("Hello", "h") >= 0.13
    >>> assert score("Hello", "H") >= 0.2

    # Acronyms are given more weight.
    # assert score("Hillsdale Michigan", "HiMi") > score("Hillsdale Michigan", "Hills")
    # assert score("Hillsdale Michigan", "Hillsd") > score("Hillsdale Michigan", "HiMi")

    """
    string = s
    if string == abbr:
        return 1.0

    scores = []
    abbr_length = len(abbr)
    string_length = len(string)
    start_of_string_bonus = False

    # walk through abbreviation
    for i, c in enumerate(abbr):

        # Find the first case-insensitive match of a character.
        c_lower = c.lower()
        c_upper = c.upper()
        index_in_string = first_valid_index(string.find(c_lower), string.find(c_upper))

        # Bail out of c is not found in string.
        if index_in_string == -1:
            return 0

        scores.append(0.1) # Set base score for matching 'c'.

        # Beginning of string bonus.

        # Case bonus
        if string[index_in_string] == c:
            scores[-1] += 0.1

        # Consecutive letter and start of string bonus.
        if index_in_string == 0:
            scores[-1] += 0.8         # increase the score when matching first char of the remainder of the string.
            # If the match is the first letter of the string and first letter of abbr.
            if i == 0:
                start_of_string_bonus = True

        # Acronym bonus
        # Weighting logic: Typing the first letter of an acronym is at most as
        # if you preceeded it by two perfect letter matches.
        if string[index_in_string - 1] == ' ':
            scores[-1] += 0.8 #* Math.min(index_in_string, 5); # cap bonus at 0.4 * 5

        # Left trim the already matched part of the string (forces sequential
        # matches)
        string = string[index_in_string + 1:-1]

    summation = sum(scores)
    # return summation/string_length  # Uncomment to weight small words higher.
    abbr_score = summation/len(scores)
    percentage_of_matched_string = abbr_length/string_length
    word_score = abbr_score * percentage_of_matched_string
    my_score = (word_score + abbr_score)/2 # softens the penalty for longer strings.
    if start_of_string_bonus and (my_score + 0.1 < 1):
        my_score += 0.1

    return my_score
