import argparse
import csv
import logging
import os
import psycopg2
from psycopg2.extensions import AsIs
import requests

def parse_args():
    parser = argparse.ArgumentParser(prog="gen_vcard.py", description="Generates employee visiting card and QR code")
    parser.add_argument("-v", "--verbose", help="Print detailed logging", action='store_true', default=False)

    subparsers = parser.add_subparsers(dest='subcommand', help='Subcommand')

    parser_init = subparsers.add_parser('initdb', help='Initialize database')
    parser_init.add_argument('-u','--user',help = 'Input user name',action = 'store',default = 'jishnu')
    parser_init.add_argument('-d', '--database', help='Database name', action='store', default='hr')
    parser_init.add_argument('-t','--table',help = 'Table name', action = 'store',default ='employees')

    parser_load = subparsers.add_parser('load',help = 'Load csv data into database')
    parser_load.add_argument('ipfile',help = 'Input file')
    parser_load.add_argument('-u','--user',help = 'Input user name',action = 'store',default = 'jishnu')
    parser_load.add_argument('-d', '--database', help='Database name', action='store', default='hr')
    parser_load.add_argument('-t','--table',help = 'Table name', action = 'store',default ='employees')

    parser_vcard = subparsers.add_parser('vcard',help = "Creating vcard ")
    parser_vcard.add_argument('-n','--number',help = "Number of vcards to generate",action = 'store',type=int,default = 10)
    parser_vcard.add_argument('-q','--qrcode',help ="To generate qr code and vcard ",action = 'store_true')
    parser_vcard.add_argument('-s','--size',help = "Size of the qr code",action = 'store',type = int ,default = 500)
    parser_vcard.add_argument('-a','--address',help = "Address in vcard",action = 'store',
                            default='100 Flat Grape Dr.;Fresno;CA;95555;United States of America')
    parser_vcard.add_argument('-u','--user',help = 'Input user name',action = 'store',default = 'jishnu')
    parser_vcard.add_argument('-d', '--database', help='Database name', action='store', default='hr')
    parser_vcard.add_argument('-t','--table',help = 'Table name', action = 'store',default ='employees')

    return parser.parse_args()

logger = None

def setup_logging(log_level):
    global logger
    logger = logging.getLogger("vcard")
    formatter = logging.Formatter("[%(levelname)s] %(asctime)s | %(filename)s:%(lineno)d | %(message)s")

    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler('run.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

def init_database(database,user):
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user= user
        )
        conn.autocommit = True

        cursor = conn.cursor()
        cursor.execute('CREATE DATABASE %s;', (AsIs(database),))
        conn.commit()
        conn.close()
        logger.info("Database %s initialized successfully",database)
    except Exception as e:
        logger.error("Error initializing database : %s",e)

def create_table(database,table,user):
    try:
        conn = psycopg2.connect(dbname = database,user = user)
        cursor = conn.cursor()
        cursor.execute ("""
                CREATE TABLE IF NOT EXISTS %s (
                id SERIAL PRIMARY KEY,
                firstname VARCHAR,
                lastname VARCHAR,
                title VARCHAR,
                email VARCHAR,
                phone_number VARCHAR
            );""",(AsIs(table),))
        conn.commit()
        logger.info("Table %s created successfully",table)
    except Exception as e:
        logger.error("Error creating table : %s",e)

def load_csv_to_database(csv_file,database,user,table):
    try:
        conn = psycopg2.connect(dbname=database,user=user)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM %s;",(AsIs(table),))
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            id = 1
            for row in reader:
                cursor.execute(f"""
                    INSERT INTO {table} (id, firstname, lastname, title, email, phone_number)
                    VALUES (%s, %s, %s, %s, %s, %s);
                """,(id,)+tuple(row))
                id+=1
        conn.commit()
        logger.info("CSV data %s loaded into the database successfully",csv_file)
    except Exception as e:
        logger.error("Error loading CSV data to database: %s".e)

def fetch_data(database,user,table):
        connection = psycopg2.connect(dbname=database, user=user)
        cursor =connection.cursor()
        cursor.execute("SELECT * from %s ",(AsIs(table),))
        data = cursor.fetchall()
        return data

def generate_vcard_content(first_name, last_name, title, email, phone_number, address):
    vcard = f"""
    BEGIN:VCARD
    VERSION:2.1
    N: {last_name};{first_name}
    FN: {first_name} {last_name}
    ORG:Authors, Inc.
    TITLE: {title}
    TEL;WORK;VOICE: {phone_number}
    ADR;WORK: {address}
    EMAIL;PREF;INTERNET: {email}
    REV:20150922T195243Z
    END:VCARD
    """
    return vcard

def generate_all_vcards(data, number, address):
    if not os.path.exists('vcards'):
        os.mkdir('vcards')
    count = 0
    for employee in data:
        count += 1
        first_name, last_name, title, email, phone_number = employee[1:]
        vcard_content = generate_vcard_content(first_name, last_name, title, email, phone_number, address)
        vcard_filename = f'{first_name}{last_name}.vcf'
        with open(os.path.join('vcards', vcard_filename), 'w') as f:
            f.write(vcard_content)
            logger.debug("%d Generated vcard for %s ", count, first_name)
        if count >= number:
            break
    logger.info("Vcard generation completed")

def generate_qrcode_content(vcard, size):
    return requests.get(f'https://chart.googleapis.com/chart?cht=qr&chs={size}x{size}&chl={vcard}').content

def generate_all_qrcodes(data, number, size):
    if not os.path.exists('vcards'):
        os.mkdir('vcards')
    count = 0
    for employee in data:
        count += 1
        first_name, last_name, title, email, phone_number = employee[1:]
        qr_filename = f'{first_name}{last_name}.qr.png'
        with open(os.path.join('vcards', qr_filename), 'wb') as file:
            file.write(generate_qrcode_content(employee, size))
            logger.debug("%d Generated QR code for %s ", count, first_name)
        if count >= number:
            break
    logger.info("QR code generation completed")

def main():
    args = parse_args()
    if args.verbose:
        setup_logging(logging.DEBUG)
    else:
        setup_logging(logging.INFO)
        setup_logging(logging.ERROR)

    if args.subcommand == 'initdb':
        init_database(args.database,args.user)
        create_table(args.database,args.table,args.user)
    if args.subcommand == 'load':
        load_csv_to_database(args.ipfile,args.database,args.user,args.table)
    if args.subcommand == 'vcard':
        data = fetch_data(args.database,args.user,args.table)
        generate_all_vcards(data,args.number,args.address)
        if args.qrcode:
            generate_all_qrcodes(data,args.number,args.size)

if __name__ =='__main__':
    main()
