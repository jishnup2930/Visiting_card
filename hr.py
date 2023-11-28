import argparse
import csv

import logging
import os
import requests
import sys

from datetime import datetime
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
    parser.add_argument('--table',help='Table name',default = 'leaves')

    subparsers = parser.add_subparsers(dest="subcommand",help='Subcommand')

    subparsers.add_parser("initdb", help="Initialize the database")

    import_parser = subparsers.add_parser("import", help="Import data in to database")
    import_parser.add_argument("employees_file", help="List of employees to import")

    query_parser = subparsers.add_parser("query", help="Get information for a single employee")
    query_parser.add_argument('employee_id',help = "Employee id ",type=int)
    query_parser.add_argument("-c",'--vcard', help="Generate vcard for employee",action="store_true", default=False)
    query_parser.add_argument('-q','--qrcode',help='Generate QR code',default=False,action='store_true')

    add_parser = subparsers.add_parser('leave',help="Add leave status of a employee")
    add_parser.add_argument('employee_id',help = "Employee id ",type=int)
    add_parser.add_argument('-d','--date',help = "Leave Date [YYYY-MM-DD]",default=datetime.today().strftime('%Y-%m-%d'))
    add_parser.add_argument('-r','--reason',help = "Reason of leave",default="Sick leave")

    count_parser = subparsers.add_parser('leave_count', help="Check remaining leave count of a employee")
    count_parser.add_argument('employee_id',help = "Employee id ",type=int)
    count_parser.add_argument("-e",'--export', help = "Export data as a csv file",action ='store_true',default = False)

    delete_parser = subparsers.add_parser('delete',help='Delete data from table')
    delete_parser.add_argument('tablename',help='Delete data from table',action= 'store')

    update_parser = subparsers.add_parser('update',help="Edit table")
    update_parser.add_argument('id',help="ID number of row")
    update_parser.add_argument('new_date',help = "Update leave Date [YYYY-MM-DD]")   
    update_parser.add_argument('new_employee_id',help = "Employee id ",type=int)
    update_parser.add_argument('new_reason',help = "Update reason of leave",type=str)

    remove_parser = subparsers.add_parser("remove",help="Remove a row from the table")
    remove_parser.add_argument('employee_id',help = "Employee id ",type=int)
    remove_parser.add_argument('date',help = "Leave Date")

    subparsers.add_parser('export',help='Export leave count of all employees')

    card_parser= subparsers.add_parser('card',help="Generate vcard and qr code (optional) for all employees")
    card_parser.add_argument('-q','--qrcode',help="Generate qr code for all employees",action = 'store_true',default=False)

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

def handle_import(args):
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
            logger.info("Data imported successfully")
    except HRException as e:
        logger.error('Error: %s',e)

def handle_query(args):
    try:
        con = psycopg2.connect(dbname=args.dbname)
        cur = con.cursor()
        cur.execute("SELECT COUNT(id) FROM employees;")
        max_employees = cur.fetchone()[0]
        if args.employee_id > max_employees:
            print(" \n    Employee ID out of range\n")
        else:
            query = "SELECT fname, lname, designation, email, phone from employees where id = %s"
            cur.execute(query, (args.employee_id,))
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
    try:
        conn = psycopg2.connect(dbname=args.dbname)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(id) FROM employees;")
        max_employees = cursor.fetchone()[0]
        if args.employee_id > max_employees:
            print("\n     Employee ID out of range.\n")
        else:    
            cursor.execute("SELECT num_of_leaves FROM designation d JOIN employees e ON d.designation_name = e.designation WHERE e.id = %s;", (args.employee_id,))
            total_leaves = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM leaves WHERE employee_id = %s;", (args.employee_id,))
            leaves_taken = cursor.fetchone()[0]

            if leaves_taken >= total_leaves:
                print("\n     No leaves left for the employee.\n")
            else:
                with open("sql/leave_update.sql") as f:
                    sql = f.read()
                    logger.debug(sql)
                cursor.execute(sql, (args.employee_id, args.date, args.reason))
                conn.commit()
                logger.info("Data inserted into leaves table successfully")
    except HRException as e:
        logger.error("Error updating data:%s",e)

def handle_leave_count(args):
    with open("sql/leave_count.sql") as f:
        sql = f.read()
        logger.debug(sql) 
    try:
        conn = psycopg2.connect(dbname=args.dbname)
        cursor = conn.cursor()
        cursor.execute(sql, (args.employee_id,))
        leaves_data = cursor.fetchone()

        if leaves_data is None:
            query = """SELECT d.num_of_leaves AS NUMBER, e.fname, e.lname, d.designation_name 
                        FROM designation d 
                        JOIN employees e 
                        ON d.designation_name = e.designation 
                        WHERE e.id = %s; """
            cursor.execute(query, (args.employee_id,))
            data = cursor.fetchone()
            if not data:
                print("\n   Employee ID not found in the list\n")
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
            leaves_taken = leaves_data[0]
            firstname = leaves_data[1]
            lastname = leaves_data[2]
            num_of_leaves = leaves_data[4]
            leaves_remaining = num_of_leaves - leaves_taken

            print(f"""
            Employee name    : {firstname} {lastname}
            Employee id      : {args.employee_id}
            Total leaves     : {num_of_leaves} 
            Leaves taken     : {leaves_taken}
            Leaves remaining : {leaves_remaining}
            \n""")

        cursor.execute('SELECT COUNT(id) FROM employees;')
        count = cursor.fetchone()[0]

        if args.export :
            if args.employee_id <= count:      
                if not os.path.exists('csv_file'):
                    os.mkdir('csv_file')
                filename = f"{args.employee_id}_leave_data.csv"
                with open(os.path.join("csv_file", filename),'w') as csvfile:
                    fieldnames = ['Employee ID', 'First Name', 'Last Name', 'Total Leaves', 'Leaves Taken', 'Leaves Remaining']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerow({
                        'Employee ID': args.employee_id,
                        'First Name': firstname,
                        'Last Name': lastname,
                        'Total Leaves': num_of_leaves if leaves_data else leaves_remaining,
                        'Leaves Taken': leaves_taken if leaves_data else 0,
                        'Leaves Remaining': leaves_remaining if leaves_data else leaves_remaining
                    })
                logger.info(f"Data exported to {filename}")
            else:
                logger.info("Employee ID is out of range for export")
    except HRException as e:
        logger.error("Error fetching leave data: %s", e)

def handle_delete(args):
    try:
        conn = psycopg2.connect(dbname=args.dbname)
        cursor = conn.cursor()
        query = "TRUNCATE TABLE %s RESTART IDENTITY CASCADE"
        cursor.execute(query,(AsIs(args.tablename),))
        conn.commit()  
        logger.info ("Data in the table %s deleted successfully",args.tablename) 
    except HRException as e:
        logger.error('Error: %s',e) 

def handle_update(args):
    try:
        conn = psycopg2.connect(dbname=args.dbname)
        cursor = conn.cursor()
        query = f"UPDATE {args.table} SET  employee_id = %s , date = %s, reason = %s  WHERE id = %s ;"
        cursor.execute(query,(args.new_employee_id,args.new_date,args.new_reason,args.id))
        conn.commit()
        logger.info("Table updated successfully")
    except HRException as e:
        logger.error("Error : %s",e)

def handle_remove(args):
    try:
        conn = psycopg2.connect(dbname=args.dbname)
        cursor = conn.cursor()
        query = f"DELETE FROM {args.table} WHERE employee_id = %s AND date = %s;"
        cursor.execute(query,(args.employee_id,args.date))
        logger.debug(query)
        conn.commit()
        if cursor.rowcount == 0:
            logger.error('No matching record found for the provided employee ID and date')
        else:
            logger.info("Row removed from table %s",args.table)
    except HRException as e:
        logger.error("Error :%s",e)

def handle_export_all_employees_leave_count_data(args):
    try:
        conn = psycopg2.connect(dbname=args.dbname)
        cursor = conn.cursor()
        query = """
            SELECT e.id, e.fname, e.lname, d.num_of_leaves, COUNT(l.employee_id) AS leaves_taken
            FROM employees e
            JOIN designation d ON d.designation_name = e.designation
            LEFT JOIN leaves l ON e.id = l.employee_id
            GROUP BY e.id, d.num_of_leaves
            ORDER BY e.id;
        """
        cursor.execute(query)
        all_leave_data = cursor.fetchall()
        filename = "all_employees_leave_data.csv"
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['Employee ID', 'First Name', 'Last Name', 'Total Leaves', 'Leaves Taken', 'Leaves Remaining']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for employee_id, fname, lname, total_leaves, leaves_taken in all_leave_data:
                leaves_remaining = total_leaves - leaves_taken
                writer.writerow({
                    'Employee ID': employee_id,
                    'First Name': fname,
                    'Last Name': lname,
                    'Total Leaves': total_leaves,
                    'Leaves Taken': leaves_taken,
                    'Leaves Remaining': leaves_remaining
                })
        logger.info("All employees leave data exported to %s",filename)
    except HRException as e:
        logger.error("Error : %s",e)

def generate_vcard_and_qrcode_for_all_employees(args):
    if not os.path.exists('vcards'):
        os.mkdir('vcards')
    con = psycopg2.connect(dbname=args.dbname)
    cur = con.cursor()
    query = "SELECT fname, lname, designation, email, phone from employees ;"
    cur.execute(query)
    data = cur.fetchall()
    
    count = 0
    for fname, lname, designation, email, phone  in data:
        count += 1
        vcard_content = generate_one_vcard(fname, lname, designation, email, phone)
        vcard_filename = f'{fname}{lname}.vcf'
        with open(os.path.join('vcards', vcard_filename), 'w') as f:
            f.write(vcard_content)
            logger.debug("%d Generated vcard for %s %s  ", count, fname ,lname)
    logger.info("VCard generated successfully")

    if args.qrcode:
        logger.info("Started QR code generation,it will take some time. Please wait..")
        if not os.path.exists('qr_code'):
            os.mkdir('qr_code')
        count = 0
        for fname, lname, designation, email, phone  in data:
            count += 1
            qr_filename = f'{fname}{lname}.qr.png'
            with open(os.path.join('qr_code', qr_filename), 'wb') as file:
                file.write(generate_one_qrcode(fname, lname, designation, email, phone))
                logger.debug("%d Generated QR code for %s %s", count, fname, lname)
        logger.info("QR codes generated successfully")

def main():
    try:
        args = parse_args()
        init_logger(args.v)
        commands = {
                "initdb" : handle_initdb,
                "import" : handle_import,
                "query" : handle_query,
                "leave" : handle_leave,
                "leave_count" : handle_leave_count,
                "delete" : handle_delete,
                "update" : handle_update,
                "remove" : handle_remove,
                "export" : handle_export_all_employees_leave_count_data,
                "card":generate_vcard_and_qrcode_for_all_employees}
        commands[args.subcommand](args)
    except HRException as e:
        logger.error("Program aborted, %s", e)
        sys.exit(-1)

if __name__ == "__main__":
    main()