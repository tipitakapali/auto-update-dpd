## Generate DPD SQLite3 Files for Tipitakapali.org

* All export-related code files have been moved to the `tpo-db` directory.

---

## Release Notes

* The apps check for new versions using live release tags, such as `v25.5.18`.
  ➤ **Remember to create a new release tag** using the current date in this format: `vYY.M.DD`.

* The apps extract and copy all files in the zip files, so we should only include the changed files.

---

## 1. For Computers

### `dpd-databases.zip`

This archive should include **all `.db` and `.js` files** from the local `db_tpo` folder:

```
dpd-databases.zip
├── abhidhan_tipitakapali.db
├── ptsped2015ed_tipitakapali.db
├── fts_tipitaka.db
├── ap_bh_mw_sanskrit.db

├── dpd_goldendict.js
├── dpd_inflection_tipitakapali.db
├── dpd_splitter_tipitakapali.db
├── dpd_synonyms_tipitakapali.db
├── dpd_tipitakapali.db

├── index.html
├── license_en.txt
└── README.md
```

---

## 2. For Flutter Mobile App

### `mobile_databases.zip`

This archive should include **all `.db` and `.json` files** (but **not** other `.zip` files) from the Flutter assets folder.

```
mobile_databases.zip
├── abhidhan_tipitakapali.db
├── ptsped2015ed_tipitakapali.db
├── fts_tipitaka.db
├── ap_bh_mw_sanskrit.db

├── db_version.json
├── dpd_inflection_tipitakapali.db
├── dpd_splitter_tipitakapali.db
├── dpd_synonyms_tipitakapali.db
├── dpd_tipitakapali.db

├── family_compound_json.json
├── family_idiom_json.json
├── family_root_json.json
├── family_set_json.json
├── family_word_json.json

├── license_en.txt
└── README.md
```


