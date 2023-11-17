import argparse
import csv
import logging
import os
import requests

def parse_args():
    parser = argparse.ArgumentParser(prog="gen_vcard.py", description="Generates employee visiting card and QR code")
    parser.add_argument("ipfile", help='Name of input file')
    parser.add_argument("-v", "--verbose", help="Print detailed logging", action='store_true', default=False)
    parser.add_argument("-n", "--number", help="Number of vcards to generate", action='store', type=int, default=10)
    parser.add_argument("-q", "--qrcode", help="Generate vcards and QR codes", action='store_true')
    parser.add_argument("-s", "--size", help="Size of QR code [100-500]", action='store', type=int, default=500)
    parser.add_argument("-a", "--address", help="Address in vcard", action='store',
                        default='100 Flat Grape Dr.;Fresno;CA;95555;United States of America')
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

def read_data(file):
    with open(file, 'r') as input_file:
        reader = csv.reader(input_file)
        return list(reader)

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

def generate_vcards(data, number, address):
    if not os.path.exists('vcards'):
        os.mkdir('vcards')
    
    count = 0
    for employee in data:
        count += 1
        first_name, last_name, title, email, phone_number = employee
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

def generate_qrcodes(data, number, size):
    if not os.path.exists('vcards'):
        os.mkdir('vcards')

    count = 0
    for employee_data in data:
        count += 1
        first_name, last_name, title, email, phone_number = employee_data
        qr_filename = f'{first_name}{last_name}.qr.png'
        with open(os.path.join('vcards', qr_filename), 'wb') as file:
            file.write(generate_qrcode_content(employee_data, size))
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
    data = read_data(args.ipfile)
    if args.qrcode:
        generate_vcards(data, args.number, args.address)
        generate_qrcodes(data, args.number, args.size)
    else:
        generate_vcards(data, args.number, args.address)

if __name__ == '__main__':
    main()
