import os

from sute import Sute

if __name__ == "__main__":
    if os.path.exists(".ses"):
        with open(".ses") as ses_file:
            ses_id = ses_file.read()
    else:
        ses_id = None

    sute = Sute(ses_id=ses_id)


    print("############# MY MAIL ############")
    for mail in sute.mails:
        print(mail)
        for message in mail.get_mail_list():
            print(message)
    print("##################################")

    print("\nCreate new address")
    new_address = sute.create_new_random_address()
    print(new_address)

    print("\nGet all domain")
    print(sute.get_all_domain())
