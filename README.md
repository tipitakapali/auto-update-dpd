### Converting dpd-deconstructor to TPO SQLite3

https://tipitakapali.org uses custom DPD database files:

```bash
dpd_synonyms_tipitakapali.db
dpd_inflection_tipitakapali.db
dpd_tipitakapali.db
dpd_splitter_tipitakapali.db 
```

This script converts the `dpd-deconstructor` tabfile into `dpd_splitter_tipitakapali.db`. The other database files are generated using this [tpo exporter](https://github.com/tipitakapali/dpd-db/tree/main/exporter/tpo)


```bash 

python3 -m venv .venv

source .venv/bin/activate

pip3 install pyglossary

# put dpd-deconstructor to tabfile dir (unzip dpd-goldendict.zip from https://github.com/digitalpalidictionary/dpd-db/releases)
pyglossary tabfile/dpd-deconstructor/dpd-deconstructor.ifo tabfile/dpd-deconstructor/dpd-deconstructor.txt --read-format=Stardict --write-format=Tabfile

python3 dpd_deconstructor_stardict_to_sqlite.py

```