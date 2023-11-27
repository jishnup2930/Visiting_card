HR management
A command-line tool for managing employee data and leave records in a PostgreSQL database.

Prerequisites
    import argparse
    import csv
    import logging
    import os
    import requests
    import sys
    import psycopg2
    from psycopg2.extensions import AsIs

Installation
pip install python3
pip install psycopg2
pip install requests


Commands
 - initdb: Initialize the database.
 - load: Load data into the database from a CSV file.
 - query: Retrieve information for a single employee.
            -c or --vcard: Generate a vCard for the employee.
            -q or --qrcode: Generate a QR code for the employee and save the data in a subdirectory qr_code
 - leave: Update leave status.
 - leave_count: Check remaining leave count.
            -e or --export : Export data as a csv file in to a subdirectory csv_file
 - delete: Delete a table.
 - update: Edit a table.
 - remove: Remove a row from a table.
 - export: Export all employees leave count data