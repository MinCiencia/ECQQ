

library(tidyverse)
library(ggplot2)
library(readxl)


# obtenemos datos mesa 
var_diags <- read_excel("input/nna_resulta.xlsx",
                        sheet = "base") %>% select(ORDEN,everything()) %>%
  janitor::clean_names() 

var_diags$organizacion <- tolower(var_diags$organizacion)

sum(is.na(var_diags$organizacion))

var_diags$rango_edades_id[var_diags$rango_edades_id==1] <- "4 a 5"
var_diags$rango_edades_id[var_diags$rango_edades_id==2] <- "6 a 9"
var_diags$rango_edades_id[var_diags$rango_edades_id==3] <- "10 a 13"
var_diags$rango_edades_id[var_diags$rango_edades_id==4] <- "14 a 18"
var_diags$rango_edades_id[var_diags$rango_edades_id==5] <- "Todos"


var_diags$contexto_id[var_diags$contexto_id==1] <- "Establecimiento Educacional"
var_diags$contexto_id[var_diags$contexto_id==2] <- "Consejo Consultivo"
var_diags$contexto_id[var_diags$contexto_id==3] <- "Oficina de Protección de Derechos"
var_diags$contexto_id[var_diags$contexto_id==4] <- "Oficina Local de la Niñez"
var_diags$contexto_id[var_diags$contexto_id==5] <- "Programa Sename"
var_diags$contexto_id[var_diags$contexto_id==6] <- "Otro"


writexl::write_xlsx(var_diags,"temp/var_diags2_inst.xlsx")
