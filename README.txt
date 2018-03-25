To run on localhost (assuming requirements previously installed):
1. Navigate to GEINOS/genios_app in terminal/cmd prompt
2. enter: export FLASK_APP=genios_app    (this will be set instead of export on Windows
3. enter: pip install -e .
4. enter: flask run

This will add the app to pip as a package that is able to be run by flask. Once running any updates will automatically
be loaded on refresh of the page