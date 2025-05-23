"""
dpd deconstruction into sqlite for tipitakapali.org
2024-06-22
last modified: 2025-04-15
"""

import os
import re
import sqlite3
from time import time as TT
import zipfile
from tpo_deconstructor_cleanup_definitions import cleanup


__version__ = "20250415"
__version_dpd__ = "20250413"

# Constants to remove non-roman words
PALI_ROMAN_CHARS = r"[ĀĪŪṀṂṆḌṬḶṚṢŚÑṄāīūṁṃṇḍṭḷṛṣśñṅA-Za-z]"
NOT_PALI_ROMAN_CHARS = r"[^ĀĪŪṀṂṆḌṬḶṚṢŚÑṄāīūṁṃṇḍṭḷṛṣśñṅA-Za-z]"
STRIP_NOT_RCHARS_END = r"[^ĀĪŪṀṂṆḌṬḶṚṢŚÑṄāīūṁṃṇḍṭḷṛṣśñṅA-Za-z]+$"


def main(batch_size=10002):
    time_log_start = TT()
    input_tab_file = os.environ.get(
        "DEC_INPUT_FILE", "tabfile/dpd-deconstructor/dpd-deconstructor.txt"
    )

    wrap_class = "dp9"

    # the table name in this log is needed later
    table_log_file = f"dpd_deconstructor_log.txt"

    dpd_splitter_tipitakapali = f"dpd_splitter_tipitakapali.db"

    print(f"\nGenerating SQLite databases: {dpd_splitter_tipitakapali}")
    print("\nIt may take a few minutes. Please wait...")

    delete_existing_databases(dpd_splitter_tipitakapali)

    table_fchars = set()
    table_s_fchars_set = set()

    conn_main = sqlite3.connect(dpd_splitter_tipitakapali)

    conn_main.execute(
        """CREATE TABLE IF NOT EXISTS misc
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT NOT NULL,
                defi TEXT NOT NULL);"""
    )

    conn_main.execute(
        """
        CREATE TABLE IF NOT EXISTS synonyms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL,
            synonym TEXT
        );
    """
    )

    conn_main.execute(
        """
        CREATE TABLE IF NOT EXISTS zmisc (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL,
            synonym TEXT
        );
    """
    )

    table_fchars.add("misc")
    table_fchars.add("synonyms")
    table_s_fchars_set.add("zmisc")

    commit_db_batch = 0
    word_counter = 0
    fill_errors = ""

    with open(input_tab_file, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            str_words, word_defi = line.strip().split("\t", 1)
            str_words = str_words.lower().strip()

            if len(str_words) < 1:
                print("* Empty word*", str_words, word_defi)
                continue

            word_list_multi_scripts = str_words.split(r"|")
            ro_1st_word = word_list_multi_scripts[0].strip()
            word = ro_1st_word

            word = strip_end_not_romanpali(word)

            if not word:
                match = re.search(r"^[\W\d_]+", ro_1st_word)
                # keep abbreviation symbols case
                if match:
                    word = ro_1st_word
                    print(" =>Non-word entry:", word)

            if not word.strip('"').strip():
                print("    ** => Skipped this entry:", word)
                continue

            # To be able to change its color when fully matched
            word_lead = f"""<span class='p1w'>{word}</span>"""

            word_counter += 1
            word_defi = cleanup(word_defi, word_counter)

            if "<script>" in word_defi:
                print("Wow, there is a script tag in the deconstructor")

            word_defi = (
                f'<section class="{wrap_class}">{word_lead}{word_defi}</section>'
            )

            # Only keep Roman script (otherwise too big db)
            synonyms_in_roman = filter_roman_pali(word_list_multi_scripts)
            synonyms_in_roman = [strip_end_not_romanpali(w) for w in synonyms_in_roman]
            synonyms_in_roman = [w.strip() for w in synonyms_in_roman if w.strip()]
            synonyms_in_roman = list(set(synonyms_in_roman))

            # synonyms
            if len(synonyms_in_roman) > 0:
                for n in range(len(synonyms_in_roman)):
                    if synonyms_in_roman[n] != word:
                        syno = synonyms_in_roman[n]
                        synonym_fchars: str = syno[0]
                        if len(syno) >= 2:
                            # z + fchars (not fchars + z)
                            synonym_fchars = "z" + syno[0:2]
                        have_alien_chars = re.search(
                            NOT_PALI_ROMAN_CHARS, synonym_fchars
                        )
                        if have_alien_chars or len(syno) == 1:
                            conn_main.execute(
                                """INSERT INTO zmisc (word, synonym)
                            VALUES (?, ?)""",
                                (word, syno),
                            )
                        else:
                            if synonym_fchars not in table_s_fchars_set:
                                table_s_fchars_set.add(synonym_fchars)
                                conn_main.execute(
                                    f"""CREATE TABLE IF NOT EXISTS {synonym_fchars}
                                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    word TEXT NOT NULL,
                                    synonym TEXT NOT NULL);"""
                                )
                            # [outside if] after created the new table, we can add now
                            conn_main.execute(
                                f"""INSERT INTO {synonym_fchars} (word, synonym)
                                VALUES (?, ?)""",
                                (word, syno),
                            )

            commit_db_batch += 1
            fchar = word[0]

            ## all in one table is very slow
            if len(word) >= 2:
                fchar = word[0:2]
                # escape SQL reserved keywords by adding a z to it
                fchar += "z"

            isW = re.search(NOT_PALI_ROMAN_CHARS, fchar)

            if isW or len(word) == 1:
                conn_main.execute(
                    f"""INSERT INTO misc (word, defi)
                VALUES (?, ?)""",
                    (word, word_defi),
                )

            else:
                if fchar not in table_fchars:
                    table_fchars.add(fchar)
                    print(f"{commit_db_batch}. {word} => New table +z:", fchar)

                    conn_main.execute(
                        f"""CREATE TABLE IF NOT EXISTS {fchar}
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    word TEXT NOT NULL,
                    defi TEXT NOT NULL);"""
                    )

                # conn_main.executemany is much faster, but not easy to code here
                # on my phone (Termux), it took about 98 seconds
                conn_main.execute(
                    f"""INSERT INTO {fchar} (word, defi)
                    VALUES (?, ?)""",
                    (word, word_defi),
                )

            if commit_db_batch % 10000 == 0:
                conn_main.commit()

                print("Committed to databases")

            if commit_db_batch % 50000 == 0:
                print("==== Another 50k words are processed", commit_db_batch, word)

    # write log file
    save_log_str = f"""Check {table_log_file}\n"""
    with open(table_log_file, "w", encoding="utf-8") as css_file:
        table_fchars.remove("misc")
        table_fchars.remove("synonyms")
        save_log_str += f"""There are {len(table_fchars)} tables in db\n. (Removed: "misc", "synonyms" in the below table): \n\nTABLE_START={str(table_fchars)}=TABLE_END"""
        save_log_str += "\n\n\n\n" + fill_errors
        css_file.write(save_log_str)

    print("All tables in db", save_log_str)
    print("Total entries", commit_db_batch)

    commit_optimize_close_db(conn_main)
    print_database_sizes(dpd_splitter_tipitakapali)

    print("\n[V] Done all! Sādhu x3.14")
    print("Took:", TT() - time_log_start, "second(s).")

    # Zip inflection DB
    zip_db(dpd_splitter_tipitakapali)


def zip_db(db_name: str):
    with zipfile.ZipFile(f"{db_name}.zip", "w") as zipf:
        zipf.write(db_name, os.path.basename(db_name))
    print(f"Zipped {db_name} into {db_name}.zip")


## helpers
def delete_existing_databases(*databases):
    for db in databases:
        if os.path.exists(db):
            print(f"\nDeleting existing database: {db}")
            os.remove(db)


def commit_optimize_close_db(*connections):
    for conn in connections:
        print("\nOptimizing the database...")
        conn.commit()
        conn.execute("PRAGMA optimize")
        conn.execute("REINDEX")
        conn.execute("VACUUM")
        conn.close()


def print_database_sizes(*databases):
    for db in databases:
        db_size_mb = os.path.getsize(db) / (1024**2)
        print(f"\nFile size of {db}: {db_size_mb:.2f} MB")


def filter_roman_pali(words: list) -> list:
    ws = [word for word in words if re.search(PALI_ROMAN_CHARS, word)]
    return [w.strip() for w in ws if w.strip()]


def strip_end_not_romanpali(word: str) -> str:
    word = re.sub(STRIP_NOT_RCHARS_END, "", word)
    # for words begin with "
    return word.strip('"').strip()


if __name__ == "__main__":
    print(
        "Hello, did you update the minified_links in cleanup_definitions.py with the replace dict from: minify_feedback_link.json before running this"
    )

    print("Starting main")
    main()
    print("Finished main")
