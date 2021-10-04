



library(tidyverse)
library(ggplot2)
library(readxl)

var_diags <- read_excel("temp/var_diags2_inst.xlsx") %>%
  janitor::clean_names()


# sacamos documento_no y orden para unir a dialogos 
var_diags_nec <- read_excel("input/nna_resulta.xlsx",
                            sheet = "necesidad") %>% select(ORDEN,everything()) %>%
  janitor::clean_names() %>% select(1,2)
var_diags_com <- read_excel("input/nna_resulta.xlsx",
                            sheet = "compromiso") %>% select(ORDEN,everything()) %>%
  janitor::clean_names() %>% select(1,2)

var_diags_prop <- read_excel("input/nna_resulta.xlsx",
                             sheet = "propuesta") %>% select(orden,everything()) %>%
  janitor::clean_names() %>% select(1,2)


# necesidades , compromisos y propuestas CLASIFICADAS EN TÓPICOS
nna_prop10 <- read_excel("input/nna_prop10.xlsx") %>% janitor::clean_names() %>% select(-1)
nna_compro10 <- read_excel("input/nna_compro10.xlsx")  %>% janitor::clean_names() %>% select(-1)
nna_nece11 <- read_excel("input/nna_nece11.xlsx") %>% janitor::clean_names() %>% select(-1)


# Añadimos variable orden

var_diags_nec <- var_diags_nec %>%
  left_join(nna_nece11, by=c("id"="document_no")) %>%
  mutate(topic=paste0("Tópic_", dominant_topic))
var_diags_comp <- var_diags_com %>%
  left_join(nna_compro10, by=c("id"="document_no")) %>%
  mutate(topic=paste0("Tópic_", dominant_topic))
var_diags_prop <- var_diags_prop %>%
  left_join(nna_prop10, by=c("id"="document_no")) %>%
  mutate(topic=paste0("Tópic_", dominant_topic))


# Ahora podemos guardar para el dashboard

var_diags_nec <- var_diags_nec %>%
  left_join(var_diags, by="orden")

var_diags_comp <- var_diags_comp %>%
  left_join(var_diags, by="orden")

var_diags_prop <- var_diags_prop %>%
  left_join(var_diags, by="orden")


write.csv(var_diags_nec ,"output/needs.csv")
write.csv(var_diags_comp ,"output/compromisos.csv")
write.csv(var_diags_prop,"output/propuestas.csv")

