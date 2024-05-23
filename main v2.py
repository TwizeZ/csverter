from termcolor import colored as col

reading_file = "contacts.csv"
writing_file = "result.csv"
vcf_file = "mtgn24.vcf"

full_data = []
missing_data_names = []


class Contact:
    def __init__(self, group, name, mtgn_name, phone, email, email_ext, ice_name, ice_phone, ice_relation):
        if "Gruppledare" in group:
            self.group = group.replace("Gruppledare ", "")
        elif "Samordnare" in group:
            self.group = group.replace("Samordnare ", "")
        elif "EKO" in group:
            self.group = group.replace("EKO-", "")
        else:
            self.group = group
        
        self.name = name
        self.mtgn_name = mtgn_name
        self.phone = phone
        self.email = email
        self.email_ext = email_ext
        self.ice_name = ice_name
        self.ice_phone = ice_phone
        self.ice_relation = ice_relation
        self.missing_data = ""

    def csv_format(self):
        return f"{self.group},{self.name},{self.mtgn_name},{self.phone},{self.email},{self.ice_name},{self.ice_phone},{self.ice_relation}"


def to_vcard(contacts_list=full_data):
    with open(vcf_file, "w", encoding="utf8") as f:
        for contact in contacts_list:
            final_name = contact.mtgn_name
            if contact.mtgn_name == "":
                final_name = contact.name.split(" ")[0]
            
            final_group = contact.group

            final_note = f"ICE {contact.ice_name} ({contact.ice_relation}): {contact.ice_phone}"

            f.write(f"BEGIN:VCARD\nVERSION:4.0\nN:{final_name};{final_group};\nORG:MTGN24\nTEL:{contact.phone}\nEMAIL:{contact.email}\nNOTE:{final_note}\nEND:VCARD\n")


def group_vcard(contacts_list=full_data):
    groups = ["ÖPH", "ARR", "INPHO", "KPH", "PHLEX", "LEK", "RSA", "VRAQUE"]
    for group in groups:
        with open(f"vCards/{group+'24'}.vcf", "w", encoding="utf8") as f:
            for contact in contacts_list:
                if group in contact.group:
                    final_name = contact.mtgn_name
                    if contact.mtgn_name == "":
                        final_name = contact.name.split(" ")[0]
                    
                    final_note = f"ICE {contact.ice_name} ({contact.ice_relation}): {contact.ice_phone}"

                    f.write(f"BEGIN:VCARD\nVERSION:4.0\nN:{final_name};{group};\nORG:MTGN24\nTEL:{contact.phone}\nEMAIL:{contact.email}\nNOTE:{final_note}\nEND:VCARD\n")


def list_entries(contacts_list=full_data):
    color = {"ÖPH": "light_grey", "ARR":"blue", "INPHO":"green", "KPH":"light_yellow", "PHLEX":"magenta",
             "LEK": "light_magenta", "RSA":"white", "VRAQUE":"yellow"}
    for i, person in enumerate(contacts_list):
        num = col(str(i+1), 'cyan')
        print(num, col(person.name + person.missing_data, color[person.group]))


def check_number(contacts_list=full_data, mode="Number/Email"):
    for contact in contacts_list:
        if mode == "Number/Email":
            phone = contact.phone
        elif mode == "ICE":
            phone = contact.ice_phone

        # Missing Phone
        if phone == "":
            print(f"{col('ERROR', 'red')}: {col(contact.name, 'yellow')} has no {mode}")
            if contact not in missing_data_names:
                contact.missing_data = f": {mode}"
                missing_data_names.append(contact)
            else:
                contact.missing_data += f", {mode}"

        # Missing Zero
        elif phone[0] == "7":
            phone = "0" + phone
            print(f"{col('FIXED', 'blue')}: {contact.name} {mode} has been fixed: {phone}")
        
        # Number including extra symbols
        elif not phone.isdigit():
            for digit in phone:
                if digit == " " or digit == "-":
                    phone = phone.replace(digit, "")
            print(f"{col('FIXED', 'magenta')}: {contact.name} {mode} has been fixed: {phone}")

        #OK
        else:
            print(f"{col('OK', 'green')}: {contact.name} {mode} is correct: {phone}")
        

        if mode == "Number/Email":
            contact.phone = phone
        elif mode == "ICE":
            contact.ice_phone = phone


def check_MTGN_name(contacts_list=full_data):
    for contact in contacts_list:
        if contact.group == "RSA":
            contact.mtgn_name = contact.name.split(" ")[0]
        elif contact.mtgn_name == "":
            contact.mtgn_name = contact.name.split(" ")[0]
            if contact.missing_data == "":
                contact.missing_data = ": MTGN Name"
            else:
                contact.missing_data += ", MTGN Name"
            
            if contact not in missing_data_names:
                missing_data_names.append(contact)

def all_except_first_empty(lst):
    return all(elem == "" for elem in lst[1:])


def read_file(file):
    with open(file, "r", encoding="utf8") as f:
        for line in f.readlines()[1:]:
            data = line.split(",")
            data.pop(-1)
            data_needed = all_except_first_empty(data)
            if not data_needed:
                new_contact = Contact(*data[:9])
                full_data.append(new_contact)


def write_file(file):
    with open(file, "w", encoding="utf8") as f:
        f.write("Group,Name,MTGN Name,Phone,Email,ICE Name,ICE Phone,ICE Relation\n")
        for data in full_data:
            f.write(f"{data.csv_format()}\n")


def main():
    read_file(reading_file)
    
    print(col("\nContacts in the file:", 'light_blue'))
    list_entries()
    
    print(col("\nLogging status for phone number:", 'green'))
    check_number()

    print(col("\nLogging status for ICE:", 'green'))
    check_number(mode="ICE")

    print(col("\nLogging status for MTGN name:", 'green'))
    check_MTGN_name()

    print(f"\n\nWriting to {col(f'{writing_file}', 'yellow')}...")
    write_file(writing_file) 
    print(f"Writing to {col(f'{vcf_file}', 'yellow')}...")
    to_vcard()
    print(f"Writing to {col(f'vCards/groups', 'yellow')}...")
    group_vcard()
    print(col("Successfully written all contacts to file!", 'green'))

    
    if len(missing_data_names) > 0:
        missing_data_names.sort(key=lambda x: x.group)
        print(col(f"\n\nMissing data for the following contacts:", 'red'))
        list_entries(missing_data_names)


main()