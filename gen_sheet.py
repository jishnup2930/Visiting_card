import csv
import sys
import faker

def generate_data():
    f = faker.Faker()
    names = []
    for i in range(40):
        record = []
        lname = f.last_name()
        fname = f.first_name()
        domain = f.domain_name()
        designation = f.job()
        email = f"{fname[:5].lower()}.{lname[:5].lower()}@{domain}"
        phone = f.phone_number()
        record = [lname, fname, designation, email, phone]
        names.append(record)
    return names

def write_file(name,data):    
    with open('employee.csv', 'w', newline='') as file: 
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    data = generate_data()
    print(data)    
    write_file(sys.argv[0], data)
