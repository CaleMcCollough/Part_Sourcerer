# @project      Metascrapper
# @copyright    Cale McCollough. All rights reserved.
# @lincense     This project is released under the GNU Public License 3.0 (http://www.gnu.org/licenses/gpl-3.0.html).
# @author       Cale McCollough
# @date         01/15/2015
# @brief        This file contains the setup script for Metascrapper
# @description  

from setuptools import setup

setup(
    name = 'Metascrapper',
    version = '0.1',
    py_modules = ['Scrapper'],
    install_requirements = [
        'Click',
    ],
    entry_points='''
        [console_scripts]
        sourcerer = Scrapper:cli
        '''
)
    