# @project      Metascrapper
# @copyright    Cale McCollough. All rights reserved.
# @lincense     This project is released under the GNU Public License 3.0 (http://www.gnu.org/licenses/gpl-3.0.html).
# @author       Cale McCollough
# @date         01/15/2015
# @brief        This file contains the Supplier class for Metascrapper.
# @description  A Supplier is a source for an EDA component.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# The way that Metascrapper handles adds and removes supplier metadata information into DipTrace is  by
# marking the supplier part variation with a a special code at the begining of each data field name.
# 
# The supplier manufacturing code is up to the user to implment.
# Supplier 0: One-off/Prototype
# Supplier 1: Assembly Run 1 Supplier Component (Or 
# Supplier 2: Assembly Run 2 Supplier Component
# ...
# Supplier N: Assembly Run N Supplier Component
# 
# This format is nice if you work with multiple assembly houses that require different packing options.
# Metascrapper Supplier Code Format
# [Supplier Number (int)][Supplier Char (char)][Alternate Char Code(char)]
# 
# The Digi-Key code is by default DK. A supplier code for a prototype unit from Digi-Key looks like this: 0DK
# The first turn-key assemply part/packing option runIndex will now be called 1DK, the sendond runIndex 2DK, etc.
#
# If is possible for users to specify alternate parts, pends a part is out of stock. Alternate parts are marked by a period, 
# and either a number, or a string 
#
# Examples:
# Supplier part number 1DK is out rigt now! We need an alternate part! 
# 
# Number example with made up part numbers
# 0D Model #, 2N700P,118
# 1D Model #, 122-a8fu7-0afh
# 2D Model #, MN-SGL-2A
# 
# Number example with made up part numbers
# 2D1 Model #, 2N700P,118
# 2D2 Model #, 122-a8fu7-0afh
# 2D3 Model #, MN-SGL-2A
# 
# String example with made up part numbers
# 2DA Model  #, 2N700P,118
# 2DB Model #, 122-a8fu7-0afh
# 2MZ Model  #, MN-SGL-2A  (MO is the code for Mouser BTW)

import DesignComponent

class ComponentSupplier():

    def __init__(self):
        HTMLParser.__init__(self)
        self.name = ''
        self.domainName = ''
    
    # @brief    function that verifies if a manufacturer code is correct
    @staticmethod
    def codeIsValid(userCode):
        if len(userCode) == 0:
            return False
        if userCode.isalnum () and (' ' in userCode) == False: # Right now I just want the other code working so I'm going to 
            return True                                        # cheat and just use alphanumeric tokens with no whitespace.
        #for char in userCode:
        #   if userCode.isalnum() is not None
        #        return False
        # 
        #stringLength = userCode.len ()
        #runIndex = ''
        #i = 0
        ## A number can have multiverify that the first block is a number.
        #while i < stringLength:
        #    if userCode[i].isnumeric():
        #        runIndex = runIndex + userCode[i]
        #if runIndex == '':
        #    return False
        #nextIndex = i + 1
        #if stringLength < nextIndex+2: # Then the string is only a number. The string must have
        #    return False
        #if userCode[nextIndex].isalpha():
        #    if userCode[nextIndex+1] == '.':
        #        return True
        #    if stringLength < nextIndex + 3 # Then there
    
    class UnitTest():
        @staticmethod
        def runUnitTest ():
            print "Running ComponentSupplier diagnostics...\n"
            
            
            
            print "\nFinished running ComponentSupplier diagnostics."

ComponentSupplier.UnitTest.runUnitTest()