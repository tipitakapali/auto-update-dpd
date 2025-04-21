## 1. Set up

```bash 

python3 -m venv .venv
source .venv/bin/activate
pip3 install pyglossary bs4

# put dpd-deconstructor to tabfile dir (unzip dpd-goldendict.zip from https://github.com/digitalpalidictionary/dpd-db/releases)

python3 main.py

```

## 2. Run

```bash

python3 main.py

```

## 3. Notes

https://tipitakapali.org uses custom DPD these database files:

```bash
dpd_synonyms_tipitakapali.db
dpd_inflection_tipitakapali.db
dpd_tipitakapali.db
dpd_splitter_tipitakapali.db 
```

This script converts the `dpd-deconstructor` tabfile into `dpd_splitter_tipitakapali.db`. 

The other database files are generated using this [tpo exporter](https://github.com/tipitakapali/dpd-db/tree/main/exporter/tpo)


- pyglossary command:

```bash 

pyglossary tabfile/dpd-deconstructor/dpd-deconstructor.ifo tabfile/dpd-deconstructor/dpd-deconstructor.txt --read-format=Stardict --write-format=Tabfile

```
