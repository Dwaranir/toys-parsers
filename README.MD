Spiders using articles, prices and old prices from /root/inputdata.csv
to search goods on sites and extract required data to .csv format.

To use you need restore python venv in /root project dir using requirements.txt

1. Git clone project

2. Make sure you are in /root folder of project and run:
   python -m venv venv

3. Activate virtual enviroment
   venv/scripts/activate

4. Restore packages using requirements.txt, just run:
   pip install -r requirements.txt

To use parcers fill the /root/inputdata.csv and run toys-parcers.bat
