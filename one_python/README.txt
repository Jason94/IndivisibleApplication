To run the script that downloads the data and populates the database, run:
  python rick_and_morty.py
from inside the "one_python" directory.

If I needed to add the ability to regularly check for new data, I would create
another script that downloads the pagination metadata for each table - the count,
the number of pages, etc. I would create a "metadata" table in the database
where I store the number of counts and pages most recently checked during a full
download.

In the "check for updates" script, if the characters, locations, or episodes have
more data than what we have recorded in our "metadata" table, we would trigger a
full download of the database. If performance was a concern, say if we expected
Rick & Morty to go on for hundreds of seasons and have millions of charactes,
then we could adjust the download script so it starts on the last page and works
backwards, stopping when we get to an ID already in the database.
