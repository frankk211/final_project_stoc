import ssl
from datetime import datetime
from prettytable import PrettyTable
import pandas as pd
import matplotlib as plt
import smtplib


class Stoc:
    """Despre gestiunea produselor"""

    categorii = {}

    def __init__(self, denp, categ, um='buc', sold=0, sold_predefinit=10):
        """metoda constructor"""
        self.sold_predefinit = sold_predefinit
        self.denp = denp
        self.categ = categ
        self.um = um
        self.sold = sold
        self.do = {}


        # la crearea unui obiect suntem informati daca soldul actual este mai mic decat soldul predefinit
        if self.sold < sold_predefinit:
            print(f"Soltul actual este {sold}.\nSoldul predefinit pentru {self.denp} este {sold_predefinit}")

        if categ in Stoc.categorii:
            self.categorii[categ] += [denp]
        else:
            self.categorii[categ] = [denp]

    def gen_cheia(self):
        if self.do:
            cheia = max(self.do.keys()) + 1
        else:
            cheia = 1
        return cheia

    def intrari(self, cant, data=str(datetime.now().strftime('%Y%m%d'))):
        cheia = self.gen_cheia()
        self.do[cheia] = [data, cant, 0]
        self.sold += cant

    def iesiri(self, cant, data=str(datetime.now().strftime('%Y%m%d'))):
        cheia = self.gen_cheia()
        if self.sold < cant:
            user_choice = input(f"Cantitatea care poate fi vanduta este: {self.sold} {self.um}\n"
                  f"Doriti sa vindeti {self.sold} {self.um} {self.denp}? y/n")
            if user_choice == "y":
                cant = self.sold
            else:
                exit()
        self.do[cheia] = [data, 0, cant]
        self.sold -= cant

    def fisap(self):
        print(f'Fisa produsului {self.denp} {self.um}')
        listeaza = PrettyTable()
        listeaza.field_names = ['Nrc', 'Data', 'Intrare', 'Iesire']
        for k, v in self.do.items():
            listeaza.add_row([k, v[0], v[1], v[2]])
        print(listeaza)
        print('Stoc final: ', self.sold)

    def graph(self):
        """ Metoda care afiseaza graficul cu intrari/iesiri dintr-o perioada pentru un anumit produs"""

        perioada = input("Introduceti perioada pentru grafic. ex: 20210303\n")
        perioada1 = perioada.split("-")[0]
        intrari = 0
        iesiri = 0

        for i in self.do.items():
            if i[1][0] == perioada1:
                intrari += int(i[1][1])
                iesiri += int(i[1][2])

        plotdata = pd.DataFrame({
        f"Intrari {perioada1}": intrari,

        f"Iesiri {perioada1}": iesiri},

        index=[f"{self.denp}"])

        plotdata.plot(kind="bar", figsize=(15, 8))

    def send_email(self):
        """Metoda care trimite e-mail cu informatii legate de fisa unui produs"""


        port = 465  #standard port for SSL
        smtp_server = "smtp.gmail.com"
        sender_email = "mioneci_claudiu12@gmail.com"
        receiver_email = "mioneci_claudiu12@yahoo.com"
        password = input("Scrieti parola si apasati enter: ")
        message = f"""
        Subject: Fisa produsului pentru {self.denp}
        {self.fisap()}
        """

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)


class DepNou(Stoc):

    def perisabilitati(self, procent):
        rulaj = 0
        for i in self.do.values():
            rulaj += i[1]
        scazaminte = rulaj * procent / 100
        self.iesiri(scazaminte)

    def val_stoc(self, pret):
        valoare = self.sold * pret
        return valoare


cuie = DepNou('cuie', 'metal', 'kg')
print(cuie.__dict__)

cuie.intrari(100, '20210303')
cuie.iesiri(23, '20210305')
cuie.iesiri(41, '20210405')
cuie.intrari(50)
cuie.iesiri(57)

# grafic = Stoc.graph(lapte)


print(cuie.__dict__)
print(cuie.do[1])

cuie.fisap()
print(cuie.categorii)

cuie.val_stoc(7)
cuie.perisabilitati(.5)

lapte = DepNou("lapte", "lactate", "litri", 3, 10)
