
reading_file = "contacts.csv"
writing_file = "result.csv"
vcf_file = "mtgn24.vcf"

full_data = []
missing_data_names = []


class Contact:
    def __init__(self, group, name, mtgn_name, phone, email, email_ext, ice_name, ice_phone, ice_relation):
        self.group = group
        self.name = name
        self.mtgn_name = mtgn_name
        self.phone = phone
        self.email = email
        self.email_ext = email_ext
        self.ice_name = ice_name
        self.ice_phone = ice_phone
        self.ice_relation = ice_relation

    def csv_format(self):
        return f"{self.group},{self.name},{self.mtgn_name},{self.phone},{self.email},{self.ice_name},{self.ice_phone},{self.ice_relation}"


def to_vcard(contacts_list=full_data):
    with open(vcf_file, "w", encoding="utf8") as f:
        for contact in contacts_list:
            final_name = contact.mtgn_name
            if contact.mtgn_name == "":
                final_name = contact.name.split(" ")[0]
            
            final_group = contact.group
            if "ÖPH" in contact.group:
                final_group = "ÖPH"
            elif "ARR" in contact.group:
                final_group = "ARR"
            elif "INPHO" in contact.group:
                final_group = "INPHO"
            elif "KPH" in contact.group:
                final_group = "KPH"
            elif "PHLEX" in contact.group:
                final_group = "PHLEX"
            elif "LEK" in contact.group:
                final_group = "LEK"
            elif "RSA" in contact.group:
                final_group = "RSA"
            elif "VRAQUE" in contact.group:
                final_group = "VRAQUE"

            final_note = f"ICE {contact.ice_name} ({contact.ice_relation}): {contact.ice_phone}"

            f.write(f"BEGIN:VCARD\nVERSION:4.0\nN:{final_name};{final_group};\nORG:MTGN24\nTEL:{contact.phone}\nEMAIL:{contact.email}\nNOTE:{final_note}\nEND:VCARD\n")


def group_vcard(contacts_list=full_data):
    groups = ["ÖPH", "ARR", "INPHO", "KPH", "PHLEX", "LEK", "RSA", "VRAQUE"]
    for group in groups:
        with open(f"vCards/{group+"24"}.vcf", "w", encoding="utf8") as f:
            for contact in contacts_list:
                if group in contact.group:
                    final_name = contact.mtgn_name
                    if contact.mtgn_name == "":
                        final_name = contact.name.split(" ")[0]
                    
                    final_note = f"ICE {contact.ice_name} ({contact.ice_relation}): {contact.ice_phone}"

                    f.write(f"BEGIN:VCARD\nVERSION:4.0\nN:{final_name};{group};\nORG:MTGN24\nTEL:{contact.phone}\nEMAIL:{contact.email}\nNOTE:{final_note}\nEND:VCARD\n")


def list_entries(contacts_list=full_data):
    for i, person in enumerate(contacts_list):
        num = str(i+1)
        if person.group == "ÖPH" or person.group == "EKO-ÖPH":
            print(num, person.name)
        elif person.group == "ARR" or person.group == "Gruppledare ARR":
            print(num, person.name)
        elif person.group == "INPHO" or person.group == "Gruppledare INPHO":
            print(num, person.name)
        elif person.group == "KPH" or person.group == "Gruppledare KPH":
            print(num, person.name)
        elif person.group == "PHLEX" or person.group == "Gruppledare PHLEX":
            print(num, person.name)
        elif person.group == "LEK":
            print(num, person.name)
        elif person.group == "RSA" or person.group == "Gruppledare RSA":
            print(num, person.name)
        elif person.group == "VRAQUE" or person.group == "Samordnare VRAQUE":
            print(num, person.name)
        else:
            print(num, person.name)


def check_number(contacts_list=full_data):
    for contact in contacts_list:
        # Phone number
        if contact.phone == "" and contact.email == "":
            print(f"ERROR: {contact.name} has no phone or email")
            missing_data_names.append(contact)
        elif contact.phone[0] == "7":
            contact.phone = "0" + contact.phone
            print(f"FIXED: {contact.name} phone number has been fixed: {contact.phone}")
        elif not contact.phone.isdigit():
            for digit in contact.phone:
                if digit == " " or digit == "-":
                    contact.phone = contact.phone.replace(digit, "")
            print(f"FIXED: {contact.name} phone number has been fixed: {contact.phone}")
        else:
            print(f"OK: {contact.name} phone number is correct: {contact.phone}")
        # ICE phone number
        if contact.ice_phone == "":
            print(f"ERROR: {contact.name} has no ICE phone")
        elif contact.ice_phone[0] == "7":
            contact.ice_phone = "0" + contact.ice_phone
            print(f"FIXED: {contact.name} ICE phone number has been fixed: {contact.ice_phone}")
        elif not contact.ice_phone.isdigit():
            for digit in contact.ice_phone:
                if digit == " " or digit == "-":
                    contact.ice_phone = contact.ice_phone.replace(digit, "")
            print(f"FIXED: {contact.name} ICE phone number has been fixed: {contact.ice_phone}")
        else:
            print(f"OK: {contact.name} ICE phone number is correct: {contact.ice_phone}")


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
        f.write("Group,Name,Meeting Name,Phone,Email,ICE Name,ICE Phone,ICE Relation\n")
        for data in full_data:
            f.write(f"{data.csv_format()}\n")


def main():
    read_file(reading_file)
    
    print("\nContacts in the file:", 'light_blue')
    list_entries()
    
    print("\nLogging status for phone number:", 'green')
    check_number()

    print(f"\n\nWriting to {writing_file}...")
    write_file(writing_file) 
    print(f"Writing to {vcf_file}...")
    to_vcard()
    print(f"Writing to vCards/groups...")
    group_vcard()
    print("Successfully written all contacts to file!", 'green')

    if len(missing_data_names) > 0:
        print("\n\nMissing data for the following contacts:", 'red')
        list_entries(missing_data_names)


if __name__ == "__main__":
    main()