# What does it do?

- when dpd has a new release -> it will auto prepare the db release files for tipitakapali.org

- will notify the API server to use the newly generated db files

- it uses a very slow "selenium" way to restore the minified dpd-goldendict version (it may take ~2 hours)


## Manual mode

If you want to manually run the scriptss, it may take 2 hours to complete. Here is the steps:


### System requirements
+ System

```bash 

sudo apt-get install -y google-chrome-stable chromium-browser

```

+ Python modules

```bash 

python -m pip install --upgrade pip
pip install pyglossary bs4 webdriver-manager selenium lxml

```

### Steps do do

Please see the [yml file](./.github/workflows/dpd_tipitakapaliorg.yml)




