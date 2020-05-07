library("tidyverse")
library("stringr")
library(rvest)

# gore afrika
af <- read_html("https://peakware.com/peaks.php?choice=AfA") %>%
  html_node('ul#peakList') %>% html_text()
af_dat <- tibble(text = unlist(str_split(af, pattern = "m\n"))) %>%
  separate(text, sep=" \\(", into=c("Gora", "Drzava")) %>% 
  separate(Drzava, sep="\\)", into=c("Drzava", "Visina")) %>%
  separate(Visina, sep=" ft/", into=c("Foots", "Metri"))

#gore antarktika
an <- read_html("https://peakware.com/peaks.php?choice=AnA") %>%
  html_node('ul#peakList') %>% html_text()
an_dat <- tibble(text = unlist(str_split(an, pattern = "m\n"))) %>%
  separate(text, sep=" \\(", into=c("Gora", "Drzava")) %>% 
  separate(Drzava, sep="\\)", into=c("Drzava", "Visina")) %>%
  separate(Visina, sep=" ft/", into=c("Foots", "Metri"))


#gore asia
as <- read_html("https://peakware.com/peaks.php?choice=AsA") %>%
  html_node('ul#peakList') %>% html_text()
as_dat <- tibble(text = unlist(str_split(as, pattern = "m\n"))) %>%
  separate(text, sep=" \\(", into=c("Gora", "Drzava")) %>% 
  separate(Drzava, sep="\\)", into=c("Drzava", "Visina")) %>%
  separate(Visina, sep=" ft/", into=c("Foots", "Metri"))

#gore asia
au <- read_html("https://peakware.com/peaks.php?choice=AuA") %>%
  html_node('ul#peakList') %>% html_text()
au_dat <- tibble(text = unlist(str_split(au, pattern = "m\n"))) %>%
  separate(text, sep=" \\(", into=c("Gora", "Drzava")) %>% 
  separate(Drzava, sep="\\)", into=c("Drzava", "Visina")) %>%
  separate(Visina, sep=" ft/", into=c("Foots", "Metri"))

#gore europa
eu <- read_html("https://peakware.com/peaks.php?choice=EuA") %>%
  html_node('ul#peakList') %>% html_text()
eu_dat <- tibble(text = unlist(str_split(eu, pattern = "m\n"))) %>%
  separate(text, sep=" \\(", into=c("Gora", "Drzava")) %>% 
  separate(Drzava, sep="\\)", into=c("Drzava", "Visina")) %>%
  separate(Visina, sep=" ft/", into=c("Foots", "Metri"))

#gore north america
na <- read_html("https://peakware.com/peaks.php?choice=NoA") %>%
  html_node('ul#peakList') %>% html_text()
na_dat <- tibble(text = unlist(str_split(na, pattern = "m\n"))) %>%
  separate(text, sep=" \\(", into=c("Gora", "Drzava")) %>% 
  separate(Drzava, sep="\\)", into=c("Drzava", "Visina")) %>%
  separate(Visina, sep=" ft/", into=c("Foots", "Metri"))

#gore south america
sa <- read_html("https://peakware.com/peaks.php?choice=SoA") %>%
  html_node('ul#peakList') %>% html_text()
sa_dat <- tibble(text = unlist(str_split(sa, pattern = "m\n"))) %>%
  separate(text, sep=" \\(", into=c("Gora", "Drzava")) %>% 
  separate(Drzava, sep="\\)", into=c("Drzava", "Visina")) %>%
  separate(Visina, sep=" ft/", into=c("Foots", "Metri"))


#gore skupaj 
gore <- bind_rows(af_dat, an_dat, as_dat, au_dat, eu_dat, na_dat, sa_dat) %>% na.omit()

#
#
#

#uvoz drzav sveta
drz <- read_html('https://www.worldometers.info/geography/how-many-countries-are-there-in-the-world/') %>%
  html_node('table') %>% html_table()

#
#
#

#