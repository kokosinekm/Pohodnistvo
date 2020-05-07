library("tidyverse")
library("stringr")
library(rvest)


#Afrika
#Atlas Mountains
af1 <- read_html('https://peakware.com/search.php') %>% 
  html_nodes(css = "ul ") %>% .[[1]] %>% html_text()

af2 <- read_html('https://peakware.com/search.php') %>% 
  html_nodes('ul li')
            
            