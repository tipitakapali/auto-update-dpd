# What does it do?

- When there is a new release of the Digital Pali Dictionary (DPD), it will automatically prepare tailored database files for tipitakapali.org. (How to monitor dpd new releases? (please google) then trigger the Action via webhook etc...)

- It will notify the API server to use the newly generated database files via a curl POST (with a secret UPDATE-KEY)

- It uses a very slow "selenium" way to restore the minified dpd-goldendict version. It may take approximately 1.x - 2 hours to complete.

## Manual mode

If you want to manually run the scripts, here are the steps:

### System requirements

+ System (for Ubuntu/Debian-based distributions)

```bash
sudo apt-get install -y google-chrome-stable
```

+ Python modules

While inside the project dir:


```bash
python3 -m venv .venv 
source .venv/bin/activate

python -m pip install --upgrade pip

pip install pyglossary bs4 webdriver-manager selenium lxml
```

### Steps to run

The entire process is defined in the [.github/workflows/dpd_tipitakapaliorg.yml](./.github/workflows/dpd_tipitakapaliorg.yml) file.
