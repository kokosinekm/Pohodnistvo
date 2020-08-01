import csv

path = "csv"
path2 = "sql"

with open(path) as csvfile:
    readCSV = csv.reader(csvfile, delimiter='"')
    next(readCSV)
    f = open(path2, "a", encoding='utf8')

    for row in readCSV:
        
        #posebni csv
        # row = row[0].split(',')

        # if len(row) == 5:
        #     prvi_pristop = row[0]
        #     ime = row[1]
        #     ime = ime.replace('\"','')
        #     visina = row[2]
        #     visina = visina.replace('\"','')
        #     gorovje = row[3]
        #     gorovje = gorovje.replace('\"','')
        #     drzava = row[4]
        #     drzava = drzava.replace('\"','')
        
        # elif len(row) > 5:
        #     ime = row[1]
        #     for i in range(3,len(row)-1):
        #         ime += row[i]
        #         leto_ustanovitve = row[-1]
        #         print(ime)
        #     visina = row[2]
        #     visina = visina.replace('\"','')
        #     gorovje = row[3]
        #     gorovje = gorovje.replace('\"','')
        #     drzava = row[4]
        #     drzava = drzava.replace('\"','')   
        #     ime = ime.replace('\"','')

        #osebe
        idn = row[0]
        ime = row[1]
        priimek = row[2]
        spol = row[3]
        starost = row[4]

        #osebe.sql dodal drustva
        #idn = row[0][:-1]
        #ime = row[1]
        #priimek = row[3]
        #spol = row[5]
        #starost = row[6][1:-1]
        #drustvo = row[7]

        f.write("insert into oseba (id, ime, priimek, spol, starost, drustvo) values ("
                + idn +",\'"+ ime +"\',\""+ priimek +"\",\'"+ spol +"\',"+ starost +",\'"+ drustvo +"\'"");\n")
    f.close()