import random
import string


class PlugLead:
    def __init__(self, letters):

        # create a new dictionary that maps the pair into both a key and a value                #
        # this ensures that the pluglead will map the value in both for either letter           #

        if letters[0].upper() == letters[1].upper():
            raise ValueError("wire can't be plug into itself")
        else:
            self.__lead = {letters[0].upper(): letters[1].upper(), letters[1].upper(): letters[0].upper()}

        # use the input letter as the key in and return the value as the encoded letter         #

    def encode(self, c):
        if c.upper() in self.__lead.keys():
            encoded = self.__lead[c.upper()]
        else:
            encoded = c
        return encoded


class Plugboard:
    # create a new dictionary that will be updated with the dictionaries from the pluglead      #
    def __init__(self):
        self.__board = {}

    def add(self, lead):
        #    set input to dictionary     #
        leads = lead.__dict__
        self.__board.update(leads['_PlugLead__lead'])
        return self.__board

        # use the input letter as the key in and return the value as the encoded letter         #

    def encode(self, c):
        c = c.upper()
        if c in self.__board.keys():
            encoded = self.__board[c.upper()]
        else:
            encoded = c
        return encoded


# This is the class that contains all functions that interact or involve the Rotors                             #
class rotor_from_name:

    # the init function focuses on converting the input data into the various formats that are used             #
    # this includes converting the strings that are inputted in the the encode_message function into lists      #
    def __init__(self, Rotors, Initials, Settings):
        initials = Initials.upper()
        self.__parts = Rotors.split()
        self.__initial_pos = initials.split()
        setting_list = Settings.split()
        self.__settings = [int(setting) for setting in setting_list]
        self.__positions = {}
        self.__adjusted_pos = {}

        #    Create all the rotors with each rotor being its own dictionary                             #
        #           each rotor is a key for its our dictionary                                          #
        #    Then the sub-dictionary uses the key as the label and value being the wire output          #
        self.__rotors = {"Beta": {"A": "L", "B": "E", "C": "Y", "D": "J", "E": "V", "F": "C", "G": "N", "H": "I",
                                  "I": "X", "J": "W", "K": "P", "L": "B", "M": "Q", "N": "M", "O": "D", "P": "R",
                                  "Q": "T", "R": "A", "S": "K", "T": "Z", "U": "G", "V": "F", "W": "U", "X": "H",
                                  "Y": "O", "Z": "S"},

                         "Gamma": {"A": "F", "B": "S", "C": "O", "D": "K", "E": "A", "F": "N", "G": "U", "H": "E",
                                   "I": "R", "J": "H", "K": "M", "L": "B", "M": "T", "N": "I", "O": "Y", "P": "C",
                                   "Q": "W", "R": "L", "S": "Q", "T": "P", "U": "Z", "V": "X", "W": "V", "X": "G",
                                   "Y": "J", "Z": "D"},

                         "I": {"A": "E", "B": "K", "C": "M", "D": "F", "E": "L", "F": "G", "G": "D", "H": "Q",
                               "I": "V", "J": "Z", "K": "N", "L": "T", "M": "O", "N": "W", "O": "Y", "P": "H",
                               "Q": "X", "R": "U", "S": "S", "T": "P", "U": "A", "V": "I", "W": "B", "X": "R",
                               "Y": "C", "Z": "J"},

                         "II": {"A": "A", "B": "J", "C": "D", "D": "K", "E": "S", "F": "I", "G": "R", "H": "U",
                                "I": "X", "J": "B", "K": "L", "L": "H", "M": "W", "N": "T", "O": "M", "P": "C",
                                "Q": "Q", "R": "G", "S": "Z", "T": "N", "U": "P", "V": "Y", "W": "F", "X": "V",
                                "Y": "O", "Z": "E"},

                         "III": {"A": "B", "B": "D", "C": "F", "D": "H", "E": "J", "F": "L", "G": "C", "H": "P",
                                 "I": "R", "J": "T", "K": "X", "L": "V", "M": "Z", "N": "N", "O": "Y", "P": "E",
                                 "Q": "I", "R": "W", "S": "G", "T": "A", "U": "K", "V": "M", "W": "U", "X": "S",
                                 "Y": "Q", "Z": "O"},

                         "IV": {"A": "E", "B": "S", "C": "O", "D": "V", "E": "P", "F": "Z", "G": "J", "H": "A",
                                "I": "Y", "J": "Q", "K": "U", "L": "I", "M": "R", "N": "H", "O": "X", "P": "L",
                                "Q": "N", "R": "F", "S": "T", "T": "G", "U": "K", "V": "D", "W": "C", "X": "M",
                                "Y": "W", "Z": "B"},

                         "V": {"A": "V", "B": "Z", "C": "B", "D": "R", "E": "G", "F": "I", "G": "T", "H": "Y",
                               "I": "U", "J": "P", "K": "S", "L": "D", "M": "N", "N": "H", "O": "L", "P": "X",
                               "Q": "A", "R": "W", "S": "M", "T": "J", "U": "Q", "V": "O", "W": "F", "X": "E",
                               "Y": "C", "Z": "K"}
                         }

    #    This function sets the initial positions of the rotors at the beginning of the encoding                #
    #    it assigns the position a value based on the difference between the character inputted and "A"         #
    def initial_positions(self):
        initial_values = []
        for rotor in range(len(self.__initial_pos)):
            rotor_pos = self.__initial_pos[rotor]
            initial_values.append(ord(rotor_pos) - ord("A"))

        for (r, i) in zip(self.__parts, initial_values):
            self.__positions[r] = i

    # This function takes the current positions of the rotors and ofsets them by the ring setting value             #
    # I also put in a check to ensure that when the rotor position goes below 0 it is increase to count down from z #
    def ring_settings(self):
        self.__adjusted_pos = self.__positions.copy()
        rotors = list(self.__adjusted_pos)

        for rotor in range(len(rotors)):
            self.__adjusted_pos[rotors[rotor]] = self.__adjusted_pos[rotors[rotor]] - self.__settings[rotor] + 1
            if self.__adjusted_pos[rotors[rotor]] < 0:
                self.__adjusted_pos[rotors[rotor]] = self.__adjusted_pos[rotors[rotor]] + 26

    # This function takes the current positions of the first rotor and increases it by 1                    #
    # if the position is at 25 it will reset to 0                                                           #
    # additionally this function is where the notches are declared and stored                               #
    # if the rotor position crosses the notch for that rotor if function will repeat for the next rotor     #
    def rotation(self):
        notches = {"I": ord("Q") - ord("A"),
                   "II": ord("E") - ord("A"),
                   "III": ord("V") - ord("A"),
                   "IV": ord("J") - ord("A"),
                   "V": ord("Z") - ord("A")}

        index = len(self.__positions) - 1
        while index != -1:
            rotor = list(self.__positions)[index]
            if self.__positions[rotor] == 25:
                self.__positions[rotor] = 0
                if rotor in notches.keys() and 25 == notches[rotor]:
                    index = index - 1
                else:
                    index = -1
            else:
                self.__positions[rotor] = self.__positions[rotor] + 1
                if rotor in notches.keys() and self.__positions[rotor] == notches[rotor] + 1:
                    index = index - 1
                else:
                    index = -1

    # This function takes in the inputted letter and sends it through each rotor from right to left     #
    def encode_right_to_left(self, c):
        letter = c.upper()
        #   This section of code is looking to check the positions of the rotors    #
        #   storing a reference for both the current and previous rotor positions   #

        #       assigns the current rotor                                               #
        for parts in reversed(range(len(self.__parts))):
            rotor = self.__parts[parts]

            #            encodes the letter based on current rotor position             #
            #            and ensures that the letter is within the A-Z range            #
            if rotor in self.__adjusted_pos.keys():
                letter = chr(ord(letter) + self.__adjusted_pos[rotor])
                if ord(letter) > 90:
                    letter = chr(ord(letter) - 26)

            #            encodes the letter based on what the next rotor would perceive the letter as   #
            #            and ensures that the letter is within the A-Z range                            #
            if letter in self.__rotors[rotor].keys():
                letter = self.__rotors[rotor][letter]
                letter = chr(ord(letter) - self.__adjusted_pos[rotor])
                if ord(letter) < 65:
                    letter = chr(ord(letter) + 26)
            else:
                letter = letter
        return letter

    # This function takes in the inputted letter and sends it through each rotor from left to right     #
    def encode_left_to_right(self, c):
        letter = c.upper()

        #   This section of code is looking to check the positions of the rotors    #
        #   storing a reference for both the current and previous rotor positions   #

        #       assigns the current rotor                                               #
        for parts in range(len(self.__parts)):
            rotor = self.__parts[parts]

            #            encodes the letter based on current rotor position             #
            #            and ensures that the letter is within the A-Z range            #
            if rotor in self.__adjusted_pos.keys():
                letter = chr(ord(letter) + self.__adjusted_pos[rotor])
                if ord(letter) > 90:
                    letter = chr(ord(letter) - 26)

            #            encodes the letter based on what the next rotor would perceive the letter as   #
            #            and ensures that the letter is within the A-Z range                            #
            if letter in self.__rotors[rotor].values():
                letter = list(self.__rotors[rotor].keys())[list(self.__rotors[rotor].values()).index(letter)]
                letter = chr(ord(letter) - self.__adjusted_pos[rotor])
            else:
                letter = letter

            if ord(letter) < 65:
                letter = chr(ord(letter) + 26)
        return letter

# This is the class that contains all functions that interact or involve the reflectors                 #
class reflector_from_name:
    def __init__(self, reflector):
        self.__reflector = reflector

        #    Create all the reflectors with each reflector being its own dictionary                     #
        #           each reflectors is a key for its our dictionary                                     #
        #    Then the sub-dictionary uses the key as the label and value being the wire output          #
        self.__reflectors = {"A": {"A": "E", "B": "J", "C": "M", "D": "Z", "E": "A", "F": "L", "G": "Y", "H": "X",
                                   "I": "V", "J": "B", "K": "W", "L": "F", "M": "C", "N": "R", "O": "Q", "P": "U",
                                   "Q": "O", "R": "N", "S": "T", "T": "S", "U": "P", "V": "I", "W": "K", "X": "H",
                                   "Y": "G", "Z": "D"},

                             "B": {"A": "Y", "B": "R", "C": "U", "D": "H", "E": "Q", "F": "S", "G": "L", "H": "D",
                                   "I": "P", "J": "X", "K": "N", "L": "G", "M": "O", "N": "K", "O": "M", "P": "I",
                                   "Q": "E", "R": "B", "S": "F", "T": "Z", "U": "C", "V": "W", "W": "V", "X": "J",
                                   "Y": "A", "Z": "T"},

                             "C": {"A": "F", "B": "V", "C": "P", "D": "J", "E": "I", "F": "A", "G": "O", "H": "Y",
                                   "I": "E", "J": "D", "K": "R", "L": "Z", "M": "X", "N": "W", "O": "G", "P": "C",
                                   "Q": "T", "R": "K", "S": "U", "T": "Q", "U": "S", "V": "B", "W": "N", "X": "M",
                                   "Y": "H", "Z": "L"}}

    #            encodes the letter based on the mapping of the reflector  #
    def encode_reflect(self, c):
        reflector = self.__reflector
        letter = c

        if letter in self.__reflectors[reflector].keys():
            letter = self.__reflectors[reflector][letter]
        else:
            letter = letter

        return letter

# This is the function that takes the settings and message that either needs to be encoded or decoded  #
def encode_message(rot, ref, intitial, settings, plugboard, c):
    #              initial set up of the machine            #
    board = Plugboard()
    wires = plugboard.split()
    #              adding all the wires to the plugboard    #
    for wire in range(len(wires)):
        board.add(PlugLead(wires[wire]))

    # set up which rotors are being used there initial position and the ring settings   #
    rotor = rotor_from_name(rot, intitial, settings)
    # set up which reflector is being used                                              #
    reflector = reflector_from_name(ref)

    message = c
    # run the function that sets the initial positions of the rotors                    #
    rotor.initial_positions()
    encoded_message_letters = []


    #              loops through all the letters in the message                         #
    for letter in message:
        #              passes the letter through the plugboard function                 #
        letter = board.encode(letter)
        #              rotates the rotors                                               #
        rotor.rotation()
        #              offset the rotors by the ring settings                           #
        rotor.ring_settings()
        #              passes the letter through the rotors right to left function      #
        letter = rotor.encode_right_to_left(letter)
        #              passes the letter through the reflector function                 #
        letter = reflector.encode_reflect(letter)
        #              passes the letter through the rotors left to right function      #
        letter = rotor.encode_left_to_right(letter)
        #              passes the letter back through the plugboard function            #
        letter = board.encode(letter)
        #              add the letter back to a new list to be converted back to a string#
        encoded_message_letters.append(letter)

    encoded_message = "".join(encoded_message_letters)
    return encoded_message


