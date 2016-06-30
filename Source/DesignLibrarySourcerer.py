# @project      Part-Sourcerer
# @copyright    Blue Storm Engineering, LLC. All rights reserved.
# @lincense     This project is released under the GNU Public License 3.0 (http://www.gnu.org/licenses/gpl-3.0.html).
# @author       Cale McCollough
# @date         01/15/2015
# @brief        This file contains the DesignLibrarySourcerer class for Part-Sourcerer
# @description  This class (will in the future) automatically generate design file libraries.
#
# Planned Featuers
#
# - User can pass in DipTrace PCB, or Schematic, and the DesignLibrarySourcerer will automatically generate component 
# libraries.
#
# - 
#
#

class DesignLibrarySourcerer():
    
    def downloadEDAFiles(self):
        print 'Downloading all EDA files to: ', sourcerer.projectDirectory
        for key, value in self.metadata:
            if currentKeyendswith(' URL') and urlContainsEDAFile(value):
                self.downloadFile(value)
    
    def downloadEDAFilesSilently(self):
        print 'Downloading all EDA files silently to: ', sourcerer.projectDirectory
        for key, value in self.metadata:
            if ' URL' in currentKey and urlContainsEDAFile(value):
                self.downloadFileSilently(value)
    
    class UnitTest ():
        @staticmethod runUnitTest():
            print 'Running DesignLibrarySourcerer.UnitTest...'
            
            
            print 'Done running DesignLibrarySourcerer.UnitTest.'