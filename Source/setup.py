# @project      Part-Sourcerer
# @copyright    Blue Storm Engineering, LLC. All rights reserved.
# @lincense     This project is released under the GNU Public License 3.0 (http://www.gnu.org/licenses/gpl-3.0.html).
# @author       Cale McCollough
# @date         01/15/2015
# @brief        This file contains the setup script for Part-Sourcerer
# @description  

from setuptools import setup

setup(
    name = 'Part-Sourcerer',
    version = '0.1',
    py_modules = ['Sourcerer'],
    install_requirements = [
        'Click',
    ],
    entry_points='''
        [console_scripts]
        sourcerer = Sourcerer:cli
        '''
)
    