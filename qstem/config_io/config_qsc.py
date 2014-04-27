__author__ = 'Michael'

"""
This file parses a qsc file (the original QSTEM config file format)
and forms its content into the standard model (a dictionary with standard keys)
"""

# Mapping of standard keys to content of qsc file
keys_to_qsc = {
    "mode": "mode:",

}

qsc_to_keys = {qsc_string: key for key, qsc_string in keys_to_qsc.iteritems()}

# nice parser from
# http://www.decalage.info/en/python/configparser
# edited a bit to convert data to integer/float types where appropriate
def parse_config(filename, comment_char="%", option_char=":"):
    options = {}
    f = open(filename)
    for line in f:
        # First, remove comments:
        if comment_char in line:
            # split on comment char, keep only the part before
            line, comment = line.split(comment_char, 1)
        # Second, find lines with an option=value:
        if option_char in line:
            # split on option char:
            option, value = line.split(option_char, 1)
            # strip spaces:
            option = option.strip()
            value = value.strip()
            try:
                value = int(value)
            except ValueError:
                try:
                    value = float(value)
                except ValueError:
                    if value == "yes":
                        value = True
                    elif value == "no":
                        value = False
                    else:
                        value = value
            # store in dictionary:
            options[option] = value
    f.close()
    return options


def read_qsc(input_filename):
    """
    Parse an input qsc file

    Returns: dict with standard (and possibly additional) keys
    """
    config = parse_config(input_filename)
    return config


def write_qsc(config_dict, output_filename):
    """
    Write a qsc file from the config_dict
    """
    with open(output_filename, "w") as f:
        for key in config_dict:
            value = config_dict[key]
            if value == True:
                value = "yes"
            elif value == False:
                value = "no"
            f.write(keys_to_qsc[key]+": "+str(value)+"\n")