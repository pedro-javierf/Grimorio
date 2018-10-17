# Grimorio
expandable python3 automation and scraping tool for UCM services (originally the library service)

## Requeriments
* Python 3.X
* BeautifulSoup 3 module
> apt-get install python3-bs4

## Configuration
* As for now, change your credentials in the global variables at main
* New functions and modules can be implemented in funcs.py, and then call them from main

## TODO (In order of preference)
- [x] Separate different functions (ie: book renew, future ones.. ;)) from main, so they can be called as functions/modules and new ones can be implemented and integrated easily
- [ ] Add error handling
- [ ] Port code to BeautifulSoup 4 syntax
- [ ] Autoboot code for Windows and Linux machines
