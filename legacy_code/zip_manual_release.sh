#!/bin/bash

# Change to the manual_db_release directory
cd ./manual_db_release || { echo "Directory not found"; exit 1; }

# Delete dpd-databases.zip if it exists
if [ -f "dpd-databases.zip" ]; then
    rm dpd-databases.zip
    echo deleted dpd-databases.zip
fi

# Create a new zip file, excluding the specified files
zip -r dpd-databases.zip * -x "dpd-databases.zip" -x "*.zip" -x "zip_script.sh"

# Move the zip file to the parent directory
echo Moving up the zip file

mv dpd-databases.zip ../
