"""
Name:        eLCS_ConfigPars.py
Authors:     Ryan Urbanowicz - Written at Dartmouth College, Hanover, NH, USA
Contact:     ryan.j.urbanowicz@darmouth.edu
Created:     November 1, 2013
Description: Manages the configuration file, by loading it, parsing it and passing values to the 'Constants' module.
             
---------------------------------------------------------------------------------------------------------------------------------------------------------
eLCS: Educational Learning Classifier System - A basic LCS coded for educational purposes.  This LCS algorithm uses supervised learning, and thus is most 
similar to "UCS", an LCS algorithm published by Ester Bernado-Mansilla and Josep Garrell-Guiu (2003) which in turn is based heavily on "XCS", an LCS 
algorithm published by Stewart Wilson (1995).  

Copyright (C) 2013 Ryan Urbanowicz 
This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the 
Free Software Foundation; either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABLILITY 
or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, 
Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
---------------------------------------------------------------------------------------------------------------------------------------------------------
"""

# Import Required Modules----------
from eLCS.Constants import cons


# ---------------------------------

class ConfigParser(object):
    """This class docstring shows how to use sphinx and rst syntax

    The first line is brief explanation, which may be completed with
    a longer one. For instance to discuss about its methods. The only
    method here is :func:`function1`'s. The main idea is to document
    the class and methods's arguments with

    - **parameters**, **types**, **return** and **return types**::

          :param arg1: description
          :param arg2: description
          :type arg1: type description
          :type arg1: type description
          :return: return description
          :rtype: the return type description

    - and to provide sections such as **Example** using the double commas syntax::

          :Example:

          followed by a blank line !

      which appears as follow:

      :Example:

      followed by a blank line

    - Finally special sections such as **See Also**, **Warnings**, **Notes**
      use the sphinx syntax (*paragraph directives*)::

          .. seealso:: blabla
          .. warnings also:: blabla
          .. note:: blabla
          .. todo:: blabla

    .. note::
        There are many other Info fields but they may be redundant:
            * param, parameter, arg, argument, key, keyword: Description of a
              parameter.
            * type: Type of a parameter.
            * raises, raise, except, exception: That (and when) a specific
              exception is raised.
            * var, ivar, cvar: Description of a variable.
            * returns, return: Description of the return value.
            * rtype: Return type.

    .. note::
        There are many other directives such as versionadded, versionchanged,
        rubric, centered, ... See the sphinx documentation for more details.

    Here below is the results of the :func:`function1` docstring.

    """

    def __init__(self, filename):
        """

        :param filename:
        """
        self.commentChar = '#'
        self.paramChar = '='
        self.parameters = self.parseConfig(filename)  # Parse the configuration file and get all parameters.
        cons.setConstants(self.parameters)  # Store run parameters in the 'Constants' module.

    def parseConfig(self, filename):
        """ Parses the configuration file. """
        parameters = {}
        try:
            f = open(filename)
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
            print('cannot open', filename)
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
