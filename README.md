# Subdah

![](assets/preview.svg)

### Search subdomains on...

* AlienVault
* AnubisDB
* Crt.sh
* DuckDuckGo
* FullHunt
* Google
* HackerTarget
* Qwant
* SecurityTrails
* Shodan
* ThreatCrowd
* ThreatMiner
* Twitter
* Yahoo

### Installation

Python >= 3.8 is required to run this program!

Using it with default Windows cmd.exe isn't recommended for emojis/live display.
I recommend to use Windows Terminal. (which is installed by default on Windows 11)

```
$ git clone https://github.com/traumatism/subdah
$ cd subdah
$ pip3 install -r requirements.txt
```

`git clone https://github.com/traumatism/subdah && cd subdah && pip3 install -r requirements.txt`

### Running

```
$ python3.10 subdah.py [--debug] -d domain.com
```

### Adding your own scanning module

1. Add a Python module in the `modules/` folder.
2. Import the required modules
```python
# Abstract classes.
from lib.common.abc import Module, Subdomain

# Manage the database.
from lib import database
```
3. Create a subclass of `Module`
```python
class MyModule(Module):

    def run(self):
        pass
```
4. Put your scanning code in the `run()` function
```python
def run(self):

    # this list should contain all the subdomains
    # gathered after running module
    subdomains: List[Subdomain] = [
        Subdomain("s1.domain.com"), 
        Subdomain("s2.domain.com")
    ]

    # add the found subdomains to the database
    for subdomain in subdomains:
        database.add_subdomain(subdomain)
```
5. Add your module to the modules list in `subdah.py`
```python
from modules.mymodule import MyModule

modules = (…, MyModule)

```
6. And you done!

### Project structure

```
.
├── assets                 assets file for README.md
│  └── preview.svg         preview svg file
├── lib                    folder containing main libraries
│  ├── __init__.py         store initialised classes
│  ├── arguments.py        manage command line arguments
│  ├── common              folder containing common libraries
│  │  └── abc.py           abstract classes
│  ├── config.py           configuration
│  ├── database.py         database manager
│  ├── logger.py           logging function
│  └── utils               folder containing utils
│     └── threading.py     threading utils
├── LICENSE                liscence
├── modules                folder containing modules
│  └── ...
├── README.md              GitHub readme file (📍 you are here!)
├── requirements.txt       Pip requirements
└── subdah.py              main program
```

### Tested on

- MacOS Monterey 12.1
- Windows 10
- Ubuntu 20.04
