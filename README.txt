To run on localhost (assuming requirements previously installed):
1. Do "pip3 install -r requirements.txt"
2. Navigate to https://github.com/agrewal707/pyorbit and follow instructions there to insall pyorbit and ncclient
2. Navigate to geinos directory, run "source pyorbit/env-setup.sh"
3. Update database location and credentials in app/__init__.py
4. Run "python3 run.py"


This will add the app to pip as a package that is able to be run by flask. Once running any updates will automatically
be loaded on refresh of the page.
