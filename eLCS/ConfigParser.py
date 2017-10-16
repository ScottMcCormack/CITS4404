from eLCS.Constants import cons


class ConfigParser(object):
    """Parse the configuration file and return it to the 'Constants' module

    Set characters for selecting and limiting config parameters.
    Parse the configuration file using :func:`parseConfig` and load into
    the eLCS.Constants module

    """

    def __init__(self, config_file):
        """ConfigParser constructor

        :param str config_file: Path to the configuration text file
        """
        self.commentChar = '#'
        self.paramChar = '='
        self.parameters = self.parseConfig(config_file)  # Parse the configuration file and get all parameters.
        cons.setConstants(self.parameters)  # Store run parameters in the 'Constants' module.

    def parseConfig(self, config_file):
        """Parse the configuration file

        Analyse the configuration file line-by-line and return a dictionary of parameters

        :param str config_file:  Path to the configuration text file
        :return: Parsed parameters
        :rtype: dict
        """

        parameters = {}
        try:
            f = open(config_file)
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
            print('cannot open', config_file)
            raise
        else:
            for line in f:
                # Remove text after comment character.
                if self.commentChar in line:
                    line, comment = line.split(self.commentChar,
                                               1)  # Split on comment character, keep only the text before the character

                # Find lines with parameters (param=something)
                if self.paramChar in line:
                    parameter, value = line.split(self.paramChar, 1)  # Split on parameter character
                    parameter = parameter.strip()  # Strip spaces
                    value = value.strip()
                    parameters[parameter] = value  # Store parameters in a dictionary

            f.close()

        return parameters
