# HR management
A command-line tool for managing employee data and leave records in a PostgreSQL database.

## Libraries need to import
    import argparse
    import csv
    import logging
    import os
    import requests
    import sys
    import psycopg2
    from psycopg2.extensions import AsIs

## Installation
    pip install python3
    pip install psycopg2
    pip install requests


## Commands
 - initdb: Initialize the database.
 - load: Load data into the database from a CSV file.
 - query: Retrieve information for a single employee.
 - leave: Update leave status.
 - leave_count: Check remaining leave count.
 - delete: Delete a table.
 - update: Edit a table.
 - remove: Remove a row from a table.
 - export: Export all employees leave count data
 - card : Generate and export all employees vcard and QR code into subdirectories named 'vcards' and 'qr_code' respectively

