import argparse
import csv
import logging
import os
import requests
import sys
import psycopg2
from psycopg2.extensions import AsIs

class HRException(Exception): pass

logger = False

def init_logger(is_verbose):
    global logger
    if is_verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO
    logger = logging.getLogger("HR")
    formatter = logging.Formatter("[%(levelname)s] %(asctime)s | %(filename)s:%(lineno)d | %(message)s")
    handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(formatter)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

def parse_args():
    parser = argparse.ArgumentParser(description="HR management")
    parser.add_argument("--dbname", help="Name of database to use", default="hr")
    parser.add_argument("-v", help="Print detailed logging", action="store_true", default=False)
    subparsers = parser.add_subparsers(dest="subcommand",help='Subcommand')
    subparsers.add_parser("initdb", help="initialise the database")

    import_parser = subparsers.add_parser("load", help="Load data in to database")
    import_parser.add_argument("employees_file", help="List of employees to import")

    query_parser = subparsers.add_parser("query", help="Get information for a single employee")
    query_parser.add_argument("-c",'--vcard', action="store_true", default=False, help="Generate vcard for employee")
    query_parser.add_argument("id", help="employee id")
    query_parser.add_argument('-q','--qrcode',help='Generate QR code',default=False,action='store_true')

    add_parser = subparsers.add_parser('leave',help="Update leave status")
    add_parser.add_argument('employee_id',help = "Employee id ")
    add_parser.add_argument('date',help = "Leave Date")
    add_parser.add_argument('reason',help = "Reason of leave")

    count_parser = subparsers.add_parser('leave_count', help="Check remaining leave count")
    count_parser.add_argument('employee_id',help = "Employee id ",type=int)
    # count_parser.add_argument("total_leave", help = "Total leave for the employee",type=int)

    delete_parser = subparsers.add_parser('delete',help='Delete table')
    delete_parser.add_argument('tablename',help='Table name',action= 'store')

    update_parser = subparsers.add_parser('update',help="Edit table")
    update_parser.add_argument ('table',help = 'Table name')
    update_parser.add_argument('employee_id',help = "Employee id ")
    update_parser.add_argument('new_date',help = "Update leave Date")
    update_parser.add_argument('new_reason',help = "Update reason of leave")


    remove_parser = subparsers.add_parser("remove",help="Remove a row from the table")
    remove_parser.add_argument('table',help='Table name')
    remove_parser.add_argument('employee_id',help = "Employee id ")
    remove_parser.add_argument('date',help = "Leave Date")

    args = parser.parse_args()
    return args

def generate_one_vcard(lname, fname, designation, email, phone):
    vcard = f"""
            BEGIN:VCARD
            VERSION:2.1
            N:{lname};{fname}
            FN:{fname} {lname}
            ORG:Authors, Inc.
            TITLE:{designation}
            TEL;WORK;VOICE:{phone}
            ADR;WORK:;;100 Flat Grape Dr.;Fresno;CA;95555;United States of America
            EMAIL;PREF;INTERNET:{email}
            REV:20150922T195243Z
            END:VCARD"""
    return vcard

def generate_one_qrcode(name, fname, designation, email, phone):    
    return requests.get (f'https://chart.googleapis.com/chart?cht=qr&chs=250x250&chl={name, fname, designation, email, phone}').content

def handle_initdb(args):
    with open("sql/init.sql") as f:
        sql = f.read()
        logger.debug(sql)
    try:
        con = psycopg2.connect(dbname=args.dbname)
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        logger.info("Tables created successfully")
    except psycopg2.OperationalError as e:
        raise HRException(f"Database '{args.dbname}' doesn't exist:{e}")

def handle_load(args):
    try:
        con = psycopg2.connect(dbname=args.dbname)
        cur = con.cursor()
        with open(args.employees_file) as f:
            reader = csv.reader(f)
            for lname, fname, designation, email, phone in reader:
                logger.debug("Inserting %s", email)
                query = "insert into employees(lname, fname, designation, email, phone) values (%s, %s, %s, %s, %s)"
                cur.execute(query, (lname, fname, designation, email, phone))
            con.commit()
            logger.info("Data loaded successfully")
    except HRException as e:
        logger.error('Error: %s',e)
        
def handle_query(args):
    try:
        con = psycopg2.connect(dbname=args.dbname)
        cur = con.cursor()
        query = "SELECT fname, lname, designation, email, phone from employees where id = %s"
        cur.execute(query, (args.id,))
        fname, lname, designation, email, phone = cur.fetchone()

        print (f"""
    Name        : {fname} {lname}
    Designation : {designation}
    Email       : {email}
    Phone       : {phone}\n""")
        
        vcard = generate_one_vcard(lname, fname, designation, email, phone)
        QR = generate_one_qrcode(lname, fname, designation, email, phone)
        if (args.vcard):
            print (f"{vcard}\n")
            
        if (args.qrcode):
            qr_filename = f'{fname}_{lname}.qr.png'
            if not os.path.exists('qr_code'):
                os.mkdir('qr_code')
            with open(os.path.join('qr_code', qr_filename), 'wb') as file:
                file.write(QR)
                logger.info("QR code generated successfully")
            
        con.close()
        logger.info("Data generated successfully")
    except HRException as e:
        logger.debug("Error : %s",e)

def handle_leave(args):
    with open("sql/leave_update.sql") as f:
        sql =f.read()
        logger.debug(sql)
    try:
        conn = psycopg2.connect(dbname=args.dbname)
        cursor = conn.cursor()
        cursor.execute(sql,(args.employee_id,args.date,args.reason))
        conn.commit()
        logger.info("Data inserted into leaves table successfully")
    except HRException as e:
        logger.error("Error updating data : %s ",e)

def handle_leave_count(args):
    with open("sql/leave_count.sql") as f:
        sql = f.read()
        logger.debug(sql) 
    try:
        conn = psycopg2.connect(dbname=args.dbname)
        cursor = conn.cursor()
        cursor.execute(sql,(args.employee_id,))     
        leaves_data = cursor.fetchone()
    
        if leaves_data is None:
            query = """SELECT d.num_of_leaves AS NUMBER, e.fname, e.lname, d.designation_name 
                            FROM designation d 
                            JOIN employees e 
                            ON d.designation_name = e.designation 
                            WHERE e.id = %s; """
            cursor.execute(query,(args.employee_id,))
            data =cursor.fetchone()
            if not data:
                print("Employee id not found in the list")
            else:
                leaves_remaining = data[0]
                firstname = data[1]
                lastname = data[2]
                leaves_taken = 0

                print(f"""
                Employee name    : {firstname} {lastname}
                Employee id      : {args.employee_id}
                Total leaves     : {leaves_remaining} 
                Leaves taken     : {leaves_taken}
                Leaves remaining : {leaves_remaining}
                \n""")

        else:
            leaves_taken =leaves_data[0]
            firstname = leaves_data[1]
            lastname =leaves_data[2]
            num_of_leaves = leaves_data[4]
            leaves_remaining = num_of_leaves - leaves_taken
            print(f"""
            Employee name    : {firstname} {lastname}
            Employee id      : {args.employee_id}
            Total leaves     : {num_of_leaves} 
            Leaves taken     : {leaves_taken}
            Leaves remaining : {leaves_remaining}
            \n""")
       
    except HRException as e:
        logger.error("Error fetching leave data: %s" ,{e})

def handle_delete(args):
    try:
        conn = psycopg2.connect(dbname=args.dbname)
        cursor = conn.cursor()
        query = "TRUNCATE TABLE %s RESTART IDENTITY CASCADE"
        cursor.execute(query,(AsIs(args.tablename),))
        conn.commit()  
        logger.info ("Data in the table %s deleted successfully",args.tablename) 
    except HRException as e:
        logger.info('Error: %s',e) 

def handle_update(args):
    try:
        conn = psycopg2.connect(dbname=args.dbname)
        cursor = conn.cursor()
        query = f"UPDATE {args.table} SET date = %s, reason = %s WHERE employee_id = %s ;"
        cursor.execute(query,(args.new_date,args.new_reason,args.employee_id))
        conn.commit()
        logger.info("Table updated successfully")
    except HRException as e:
        logger.info("Error : %s",e)
def handle_remove(args):
    try:
        conn = psycopg2.connect(dbname=args.dbname)
        cursor = conn.cursor()
        query = f"DELETE FROM {args.table} WHERE employee_id = %s AND date = %s;"
        cursor.execute(query,(args.employee_id,args.date))
        conn.commit()
        logger.info("Row removed from table %s",args.table)
    except HRException as e:
        logger.info("Error :%s",e)

def main():
    try:
        args = parse_args()
        init_logger(args.v)
        commands = {"initdb" : handle_initdb,
               "load" : handle_load,
               "query" : handle_query,
               "leave" : handle_leave,
               "leave_count" : handle_leave_count,
               "delete" : handle_delete,
               "update" : handle_update,
               "remove" : handle_remove}
        commands[args.subcommand](args)
    except HRException as e:
        logger.error("Program aborted, %s", e)
        sys.exit(-1)
    

if __name__ == "__main__":
    main()