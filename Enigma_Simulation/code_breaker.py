from enigma import *


# This is the function that was used to solve code 1 and is completed by looping through the 3 possible reflectors
def code1():
    for ref in ["A", "B", "C"]:
        crib = "SECRETS"
        message = encode_message("Beta Gamma V", ref, "M J M", "04 02 14", "KI XN FL",
                                 "DMEXBMKYCVPNQBEDHXVPZGKMTFFBJRPJTLHLCHOTKOYXGGHZ")

        # check if the encoded message contains the crib                                #
        if crib in message:
            print("The message = " + message)
            print("The correct Reflector = " + ref)
            break


# This is the function that was used to solve code 2
# This is completed by looping through the possible combinations of the initial positions
# These are generated buy using the itertools.product function on a list of the alphabet
def code2():
    import itertools
    for settings_option in itertools.product(string.ascii_uppercase, repeat=3):
        start_positions_list = settings_option
        start_positions = " ".join(start_positions_list)
        crib = "UNIVERSITY"
        message = encode_message("Beta I III", "B", start_positions, "23 02 10", "VH PT ZG BJ EY FS",
                                 "CMFSUPKNCBMUYEQVVDYKLRQZTPUFHSWWAKTUGXMPAMYAFITXIJKMH")

        # check if the encoded message contains the crib                                #
        if crib in message:
            print("The message = " + message)
            print("The correct starting positions for code 2 = " + start_positions)
            break


# This is the function that was used to solve code 3
def code3():
    import itertools
    # create 2 lists of the potential rotors and the potential rotor settings                   #
    rotors_options_list = ["II", "IV", "Beta", "Gamma"]
    settings_options_list = ["02", "04", "06", "08", "20", "22", "24", "26"]

    # loop through all possible combinations of the rotors without repeating a rotor            #
    # These combinations are made using the itertools.permutations function                     #
    for rotor_option in itertools.permutations(rotors_options_list, 3):

        # loop through the the reflector options                                                #
        for ref in ["A", "B", "C"]:

            # loop through all possible combinations of the ring setting                        #
            # These combinations are made using the itertools.product function                  #
            for settings_option in itertools.product(settings_options_list, repeat=3):

                # convert all these inputs back into a format that can be used by the encode_message function   #
                rotor_option_list = list(rotor_option)
                rotor_order = " ".join(rotor_option_list)
                settings_option_list = list(settings_option)
                settings = " ".join(settings_option_list)
                crib = "THOUSANDS"
                message = encode_message(rotor_order, ref, "E M Y", settings, "FH TS BE UQ KD AL",
                                         "ABSKJAKKMRITTNYURBJFWQGRSGNNYJSDRYLAPQWIAGKJYEPCTAGDCTHLCDRZRFZHKNRSDLNPFPEBVESHPY")

                # check if the encoded message contains the crib                                #
                if crib in message:
                    print("The message = " + message)
                    print("The correct rotors and order = " + rotor_order + "\nThe correct reflector = " + ref +
                          "\nThe correct settings = " + settings)
                    break
            else:
                continue
            break
        else:
            continue
        break

# This is the function that was used to solve code 3
def code4():
    # create a list of all the letters that are already being used              #
    import itertools
    wires = "WP RJ A? VF I? HN CG BS"
    letter_list = wires.replace("?", "")
    letter_list = letter_list.replace(" ", "")
    letter_list = set(letter_list)

    alphabet = set(string.ascii_uppercase)

    # remove the letters that are being used from a list of the alphabet        #
    available_letters_a = alphabet - letter_list
    available_letters_a = list(available_letters_a)
    available_letters_a.sort()

    # loop through all possible remaining letters to pair with "A"             #
    for letter1 in available_letters_a:
        wire1 = "A" + letter1
        available_letters_b = available_letters_a.copy()

        # Remove the letter that is used from a copy of the list                   #
        available_letters_b.remove(letter1)

        # loop through all possible remaining letters to pair with "I"             #
        for letter2 in available_letters_b:
            wire2 = "I" + letter2

            # recreate the string of pair to be put back into the function         #
            board = "WP RJ " + wire1 + " VF " + wire2 + " HN CG BS"
            crib = "TUTOR"

            # These words were added to the function with each iteration of the code to reduce the number of outcomes  #
            identified_word1 = "EXAMPLES"
            identified_word2 = "DURING"
            message = encode_message("V III IV", "A", "S W U", "24 12 10", board,
                                     "SDNTVTPHRBNWTLMZTQKZGADDQYPFNHBPNHCQGBGMZPZLUAVGDQVYRBFYYEIXQWVTHXGNW")
            # check if the encoded message contains the crib                                #
            if crib in message and identified_word1 in message and identified_word2 in message:
                print("The message = " + message)
                print("The correct Plugboard pairs = " + board)



code1()
code2()
code3()
code4()
