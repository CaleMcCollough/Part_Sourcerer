# Part Sourcerer
An open-source set of tools for managing parts for Bills of Materials and 
design components written in Python. Part Sourcerer works by entering in the 
web address for a part on a supplier's website (currently only works with 
digikey.com). Software then extracts all metadata from supplier's website, and 
downloads datasheets and 3D models into customizable folder structures. (In the 
future) The user can also enter in the search entry they used to search for the 
cheapest part, and the software will automatically suggest cheaper parts. Right 
now this software is being developed to use with DipTrace (diptrace.com), but I 
would like to integrate other PCB CAD software.

## License
Copyright © 2016 [Cale McCollough](mailto:cale.mccollough@gmail.com).
	All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
