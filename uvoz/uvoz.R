library(rvest)
library(dplyr)

#uvoz 
gore <- read_html('https://en.wikipedia.org/wiki/List_of_first_ascents') %>%
  html_nodes('table') %>% .[[1]] %>% html_table()
gor_dr1 = c('Filipini','Slovenija','Japonska','Iran','Francija','Nemcija','Italija','Svica','Francija','Argentina','Juzna Afrika','Mehika','Svica','Francija','Svica','Italija','Avstrija','Ekvador','Slovaska','Zdruzene Drzave Amerike','Avstrija','Svica','Svica','Italija','Avstrija','Ekvador','Svica','Islandija','Slovenija','Avstrija','Francija','Velika Britanija','Slovaska','Slovenija','Italija','Avstrija','Svica','Francija','Svica','Italija','Francija','Rusija','Svica','Svica','Spanija','Svica','Avstrija','Avstrija','Avstrija','Nemcija','Filipini','Spanija','Zdruzene Drzave Amerike','Italija','Francija','Svica','Svica','Avstrija','Zdruzene Drzave Amerike','Italija','Nemcija','Avstrija','Svica','Kanada','Francija','Avstrija','Italija','Rusija','Svica','Turcija','Avstrija','Avstrija','Avstrija','Slovaska','Svica','Svica','Avstrija','Avstrija','Francija','Nova Zelandija','Slovaska','Etiopija','Norveska','Avstrija','Spanija','Svica','Zdruzene Drzave Amerike','Avstrija','Svica','Avstrija','Svica','Avstrija','Azerbajdzan','Mehika','Avstrija','Svica','Norveska','Svica','Dominikanska republika','Zdruzene Drzave Amerike','Zdruzene Drzave Amerike','Italija','Avstrija','Zdruzene Drzave Amerike','Svica','Svica','Zdruzene Drzave Amerike','Svica','Italija','Svica','Svica','Svica','Svica','Svica','Italija','Svica','Francija','Italija','Italija','Svica','Svica','Italija','Francija','Kamerun','Svica','Avstrija','Italija','Italija','Italija','Italija','Francija','Svica','Svica','Italija','Italija','Zdruzene Drzave Amerike','Svica','Francija','Svica','Italija','Avstrija','Italija','Francija','Gruzija','Zdruzene Drzave Amerike','Zdruzene Drzave Amerike','Italija','Italija','Avstrija','Francija','Zdruzene Drzave Amerike','Zdruzene Drzave Amerike','Zdruzene Drzave Amerike','Ekvador','Zdruzene Drzave Amerike','Rusija','Zdruzene Drzave Amerike','Zdruzene Drzave Amerike','Zdruzene Drzave Amerike','Norveska','Francija','Poljska','Francija','Nova Zelandija','Francija','Ekvador','Ekvador','Ekvador','Filipini','Francija','Francija','Svedska','Indija','Italija','Malezija','Rusija','Gruzija','Papuanska Nova Gvineja','Tanzanija','Mehika','Kanada','Zdruzene drzave Amerike','Kanada','Nova Zelandija','Nova Zelandija','Italija','Argentina','Argentina','Kanada','Zdruzene drzave Amerike','Bolivija','Kitajska','Italija','Kenija','Kanada','Iran','Kanada','Kanada','Kanada','Zdruzene drzave Amerike','Gruzija','Demokraticna Republika Kongo','Zdruzene drzave Amerike','Zdruzene drzave Amerike','Tanzanija','Uganda','Indija','Zdruzene drzave Amerike','Antarktika','Islandija','Zdruzene drzave Amerike','Peru','Nova Zelandija','Zdruzene drzave Amerike','Norveska','Nova Zelandija','Indija','Peru','Uganda','Zdruzene drzave Amerike','Kanada','Tanzanija','Papuanska Nova Gvineja','Poljska','Zdruzene drzave Amerike','Kanada','Grcija','Kazahstan','Kanada','Zdruzene drzave Amerike','Kanada','Bolivija','Bolivija','Zdruzene drzave Amerike','Zdruzene drzave Amerike','Zdruzene drzave Amerike','Zdruzene drzave Amerike','Maroko','Zdruzene drzave Amerike','Kanada','Kanada','Zdruzene drzave Amerike','Demokraticna Republika Kongo','Bolivija','Zdruzene drzave Amerike','Kirzigistan','Indija','Zdruzene drzave Amerike','Kanada','Indija','Kazahstan','Alzirija','Peru','Peru','Peru','Kitajska','Tadzikistan','Argentina','Zdruzene drzave Amerike','Kitajska','Venezuela','Grenlandija','Nepal','Kanada','Kanada','Peru','Indija','Indija','Indonezija','Argentina','Butan','Kanada','Zdruzene drzave Amerike','Indija','Zdruzene drzave Amerike','Zdruzene drzave Amerike','Zdruzene drzave Amerike','Papuanska Nova Gvineja','Kirzigistan','Kazahstan','Kolumbija','Kolumbija','Indija','Indija','Bolivija','Zdruzene drzave Amerike','Bolivija','Zdruzene drzave Amerike','Argentina','Kanada','Zdruzene drzave Amerike','Peru','Kanada','Nepal','Pakistan','Peru','Kanada','Argentina','Kanada','Kanada','Peru','Peru','Cile','Nepal','Nepal','Pakistan','Kanada','Peru','Indija','Zdruzene drzave Amerike','Zdruzene drzave Amerike','Pakistan','Nepal','Kitajska','Nepal','Nepal','Nepal','Nepal','Nepal')
gor_dr2 = c('Kitajska','Pakistan','Peru','Kitajska','Peru','Nepal','Pakistan','Pakistan','Peru','Peru','Cile','Pakistan','Pakistan','Pakistan','Pakistan','Pakistan','Pakistan','Pakistan','Indonezija','Nepal','Nepal','Nepal','Pakistan','Pakistan','Kanada','Afganistan','Afganistan','Nepal','Nepal','Zdruzene Drzave Amerike','Antarktika','Indija','Indonezija','Nepal','Cile','Ekvador','Zdruzene Drzave Amerike','Mongolija','Cile','Nepal','Kitajska','Zdruzene Drzave Amerike','Zdruzene Drzave Amerike','Antarktika','Nova Zelandija','Kanada','Kanada','Kanada','Brazilija','Velika Britanija','Antarktika','Antarktika','Kanada','Pakistan','Nepal','Nepal','Pakistan','Pakistan','Indija','Argentina','Indija','Indija','Indija','Pakistan','Indija','Pakistan','Kitajska','Argentina','Pakistan','Pakistan','Pakistan','Pakistan','Nepal','Nepal','Indija','Pakistan','Pakistan','Pakistan','Kanada','Antarktika','Kitajska','Kitajska','Kitajska','Kitajska','Pakistan','Indija','Zdruzene Drzave Amerike','Kitajska','Butan','Kitajska','Kitajska','Kanada','Kitajska','Antarktika','Indija','Kitajska','Antarktika','Kitajska','Antarktika','Kitajska','Kitajska','Kitajska','Antarktika','Pakistan','Antarktika','Indija','Antarktika','Antarktika','Pakistan','Burma','Antarktika','Butan','Indija','Kitajska','Nepal','Kitajska','Antarktika','Antarktika','Indija','Indija','Pakistan','Burma','Pakistan','Nepal')
gore$Country <- c(gor_dr1, gor_dr2)
gore$`Date [1]` <- as.numeric(regmatches(gore$`Date [1]`, regexpr('[0-9]{3,4}', gore$`Date [1]`, perl = TRUE)))

#dodal enega ki je pred nasim stetjem
gore$`Date [1]`[1] <- '2000 BC'

# dodajanje osamelcev
gore$Range[3]
gore$Range[gore$Range == ""] <- 'osamelec'

gore <- data.frame(gore$`Date [1]`, gore$Peak, gore$`Height (m)`, gore$Range, gore$Country)
colnames(gore) <-  c('Prvi pristop', 'Ime', 'Visna', 'Gorovje', 'Drzava')
write.csv(gore, "C:\\Users\\komp\\Documents\\FMF\\opb\\Pohodnistvo\\Podatki\\Gore.csv", row.names = FALSE)


#################################################################################################################



#uvoz drzav sveta
drz <- read_html('https://www.worldometers.info/geography/how-many-countries-are-there-in-the-world/') %>%
  html_node('table') %>% html_table()


#imena drzav spremenimo v Slovenscino
imena <- read_html('https://www.101languages.net/slovenian/country-names-slovenian/') %>%
  html_nodes('table') %>% .[[1]] %>% html_table()

drzave <- left_join(imena, drz, by=c('English'='Country'))

#dodal tri omembne drzave
ZDA <- drz[3,]
drzave[185,] <- c(drzave$English[185], drzave$Slovenian[185], ZDA$`#`, ZDA$`Population(2020)`, ZDA$`World Share`, ZDA$`Land Area (Km²)`)

DRkongo <- drz[16,]
drzave[45,] <- c(drzave$English[45], drzave$Slovenian[45], DRkongo$`#`, DRkongo$`Population(2020)`, DRkongo$`World Share`, DRkongo$`Land Area (Km²)`)

ceska <- drz[85,]
drzave[44,] <- c(drzave$English[44], drzave$Slovenian[44], ceska$`#`, ceska$`Population(2020)`, ceska$`World Share`, ceska$`Land Area (Km²)`)

#drop NA
drzave <- na.omit(drzave)
drzave <- data.frame(drzave$Slovenian, drzave$`Population(2020)`, drzave$`Land Area (Km²)`)
colnames(drzave) <-  c('Drzava', 'Populacija(2020)', 'Povrsina(Km2)')
write.csv(drzave, "C:\\Users\\komp\\Documents\\FMF\\opb\\Pohodnistvo\\Podatki\\Drzave.csv", row.names = FALSE)

#gorovja uvoz
gorovje <- data.frame(unique(gore$Gorovje))
colnames(gorovje) <-  c('Gorovje')
write.csv(gorovje, "C:\\Users\\komp\\Documents\\FMF\\opb\\Pohodnistvo\\Podatki\\Gorovje.csv", row.names = FALSE)

###########################################################################################################################################
#uvozimo osebe in jim dodamo drustva

osebe <- read.csv("C:\\Users\\komp\\Documents\\FMF\\opb\\Pohodnistvo\\Podatki\\Osebe.csv")
osebe <- data.frame(osebe$id, osebe$Ime, osebe$Priimek, osebe$Spol, osebe$Starost) 
colnames(osebe)<-c('id', 'Ime', 'Priimek', 'Spol', 'Starost')

drustva <- read.csv("C:\\Users\\komp\\Documents\\FMF\\opb\\Pohodnistvo\\Podatki\\Drustva.csv")$id
imena_drustev <- sapply(strsplit(as.character(drustva), '"'), `[`, 2)
letnica_nastanka <- sapply(strsplit(as.character(drustva), '"'), `[`, 3) %>% substring(., 2) %>% as.numeric(.)
nastanek <- data_frame('Drustvo' = imena_drustev, 'Leto ustanovitve' = letnica_nastanka
                       )
#razporedimo osebe po drustvih
#ne ponavljaj!!!!
#zato ker vzorec dolocen nakljucno
vzorec <- sample(imena_drustev, length(osebe$id), replace = TRUE)
osebe_nove <- bind_cols(osebe, 'Drustvo' = vzorec)
#write.csv(osebe_nove, "C:\\Users\\komp\\Documents\\FMF\\opb\\Pohodnistvo\\Podatki\\Osebe.csv", row.names = FALSE)

clani <- data_frame(osebe_nove$id, osebe_nove$Drustvo) %>% group_by(., osebe_nove$Drustvo) %>% summarise('stevilo clanov' = n())
colnames(clani) <- c('Drustvo', 'stevilo clanov')
drustva_nova <- left_join(nastanek, clani, by='Drustvo')
#write.csv(drustva_nova, "C:\\Users\\komp\\Documents\\FMF\\opb\\Pohodnistvo\\Podatki\\Drustva.csv", row.names = FALSE)
