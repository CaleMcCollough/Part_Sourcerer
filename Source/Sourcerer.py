# @project      Part-Sourcerer
# @copyright    Blue Storm Engineering, LLC. All rights reserved.
# @lincense     This project is released under the GNU Public License 3.0 (http://www.gnu.org/licenses/gpl-3.0.html).
# @author       Cale McCollough
# @date         01/15/2015
# @brief        This file contains the Part-Sourcerer class and command-line application
# @description  Part-Sourcerer is a set of Electronic Design Automation tools written in Python.
#
# Supported File Formats:
# Part-Sourcerer currently only supports the DipTrace ASCII file format(in progress. See www.diptrace.com), but in the future will 
# supprt exporting to Altium Designer.
# 
# Current Features List:
#
# - Design files importing from the digikey.com
# Future web, design componetn library geer, BOM cost optimization, and documenation exportation. that uses the DipTrace file 
#               format.The purpose of Part-Sourcerer is to serve as an automation tool for processing EDA design files. Part-Sourcerer is really
#

''' Native APIs '''
import os
import sys
import string
import urllib2

''' Third-Party APIs '''
import click
import requests


@click.command()
@click.option('-s', default='', help = 'This option runs the EDA Sourcerer on the specified.')
@click.option('-app', default='', help = 'The name of the EDA Application.')
def cli(libraryFilename, edaSoftareType):
    """Welcome to the Electronics Design Automation Sourcerer."""
    click.echo('Hello world' + string)

class Sourcerer():
    ''' Static variabls '''
    validChars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    
    @staticmethod
    def getTerminalSize():
        env = os.environ
        def ioctl_GWINSZ(fd):
            try:
                import fcntl, termios, struct, os
                cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
            except:
                return
            return cr
        cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
        if not cr:
            try:
                fd = os.open(os.ctermid(), os.O_RDONLY)
                cr = ioctl_GWINSZ(fd)
                os.close(fd)
            except:
                pass
        if not cr:
            cr = (env.get('LINES', 25), env.get('COLUMNS', 80))

            ### Use get(key[, default]) instead of a try/catch
            #try:
            #    cr = (env['LINES'], env['COLUMNS'])
            #except:
            #    cr = (25, 80)
        return int(cr[1]), int(cr[0])
    
    @staticmethod
    def printLine(char):
        (width, height) = Sourcerer.getTerminalSize()
        line = ''
        for i in range(0, width):
            line += char
        print line
    
    @staticmethod
    def manufacturerCodeIsValid(userCode):
        if len(userCode) == 0:
            return False
        for char in userCode:
            if not char.isalnum():
                return False
        return True
    @staticmethod
    def filenameOfURL(url):
        pass
        
    @staticmethod
    def fixFilename(filename):
        valueURL = ''.join(c for c in filename if c in Sourcerer.validChars)
        #print properURL
        return valueURL
    
    # @brief    Function that check if a filename is valid on the executing OS.
    @staticmethod
    def pathIsValid(filename):
        try:
            #print 'filename is valid: ', filename
            open(filename, 'w').close()
            os.unlink(filename)
            return True
        except OSError: # Not needed but left for copy and paste purposes later.
            #print 'Error: filename not valid: ', filename
            return False
        return False
    
    # @brief    Function that saves that give data to the a specified filename
    @staticmethod
    def saveToFile(data, filename):
        if not Sourcerer.pathIsValid(filename):
            print 'Error: Filename not valid: ', filename
            return
        print 'Saving data to file: ', filename
        
        file = open(filename, 'w')
        file.write(data)
        file.close
    
    # @brief    Function that checks to see if a directory exists, and 
    @staticmethod
    def cleanDirecoryPath(directoryPath):
        if os.path.isdir(directoryPath):
            return directoryPath
        return '/'
    
    # @brief    Function that uses the Requests API to load an entire webpage.
    @staticmethod
    def loadContentFromURL(url):
        print 'Loading conent from URL: ', url
        htmlDoc = requests.get(url).content
        return htmlDoc
    
    @staticmethod
    def fileNameIsValid(fileName):
        try:
            open(filename, 'w').close()
            os.unlink(filePath)
            return True
        except OSError:
            return False
        return False
    
    # Method that adds an http:
    @staticmethod
    def fixShortURL(url):
        print '$$$>>> url = ', url
        if url.startswith('www.'): # We need to add an 'http://'
            print 'Fixing short URL: ', url
            return 'http://' + url
        
        if url.startswith('http://'):
            return url
        
        print 'Fixing short URL: ', url
        # Then add 'http://www.' to the directory
        return 'http://www.' + url
    
    @staticmethod
    def checkPathExistsOrCreate(filePath):
        if not os.path.exists(directory): # Then create the directory.
            print 'Path does not exist. Creating directory for: ', directory
            os.makedirs(directory)
    
    # Function that returns the filetype of a url.
    @staticmethod
    def getFiletype(url):
        designFilename = url.split('/')[-1]
        designFiletype = designFilename.split('.')[-1]
        return designFiletype
    
    @staticmethod
    def downloadFile(url, filename):
        filename = url.split('/')[-1]
        u = urllib2.urlopen(url)
        f = open(filename, 'wb')
        meta = u.info()
        fileSize = int(meta.getheaders("Content-Length")[0])
        print "Downloading: %s Bytes: %s" % (filename, fileSize)

        fileSize_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            fileSize_dl += len(buffer)
            f.write(buffer)
            status = r"%10d  [%3.2f%%]" % (fileSize_dl, fileSize_dl * 100. / fileSize)
            status = status + chr(8)*(len(status)+1)
            print status,

        f.close()
        return
        
    class UnitTest():
        @staticmethod
        def runUnitTest ():
            print "Running Sourcerer.UnitTest...\n"
            
            #edaTools = Sourcerer()
        
            print "Done running Sourcerer.UnitTest.\n"

Sourcerer.UnitTest.runUnitTest()