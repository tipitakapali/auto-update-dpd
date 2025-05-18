# main.py
import subprocess
from tpo_deconstructor_to_sqlite import main
import os


def run_pyglossary():
    if os.path.exists("tabfile/dpd-deconstructor/dpd-deconstructor.txt"):
        prompt = input(
            """The file 'tabfile/dpd-deconstructor/dpd-deconstructor.txt' already exists. Do you want to overwrite it? (y/n): """
        )
        if prompt.lower() != "y":
            return
    print("""Running pyglossary to convert the Stardict format to Tabfile.""")
    command = [
        "pyglossary",
        "tabfile/dpd-deconstructor/dpd-deconstructor.ifo",
        "tabfile/dpd-deconstructor/dpd-deconstructor.txt",
        "--read-format=Stardict",
        "--write-format=Tabfile",
    ]
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        print("pyglossary conversion successful.")
    except subprocess.CalledProcessError as e:
        print(f"pyglossary conversion failed: {e}")
        print("Standard Output:\n", e.stdout)
        print("Standard Error:\n", e.stderr)
    except FileNotFoundError:
        print(
            "Error: pyglossary command not found.  Ensure it is installed and in your PATH."
        )
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    run_pyglossary()
    main()
    print("Remember to update cleanup_definitions.py")
