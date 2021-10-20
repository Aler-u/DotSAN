setwd('~/Documents/Proyectos/Grafo SAN/mincyt_datasets/')

library(tidyverse)

#Vectores que contienen los nombres de los archivos csv de interes segun un regex como argumento de pattern
personas_files <- list.files(pattern = "personas_\\d")
indicadores_files <- list.files(pattern = "personas_indicadores_genero_\\d")

#Dataframes vacios para contener los resultados finales de la iteracion
personas_year <- tibble()
indicadores_year <- tibble()

#Loop:
  #lee un archivo de cada vector
  #"pega" (pega las rows de ambos dataframes) a los dataframes vacios que se van llenando con cada iteracion
for(i in 1:8){
  tmp_personas <- read_csv2(personas_files[i])
  tmp_indicadores <- read_csv2(indicadores_files[i])
  personas_year <- rbind(personas_year, tmp_personas)
  indicadores_year <- rbind(indicadores_year, tmp_indicadores)
}

#Modifico el nombre de la columna correspondiente al año para que sea igual en ambos datasets
personas_year <- personas_year %>%
  rename(anio_id = anio)

#Referencias
categoria_conicet <- read_csv2('ref_categoria_conicet.csv')
disciplina <- read_csv2('ref_disciplina.csv')
grado_academico <- read_csv2('ref_grado_academico.csv')
sexo <- read_csv2('ref_sexo.csv')
condicion_docente <- read_csv2('ref_tipo_condicion_docente.csv')
tipo_personal <- read_csv2('ref_tipo_personal.csv')

#Union
indicadores_personas <- full_join(x = personas_year, y = indicadores_year, by = c("persona_id", "anio_id"))

#Union referencias
indicadores_personas_ref <- left_join(x = indicadores_personas, y = sexo, by = 'sexo_id') %>%
  left_join(x =., y = grado_academico, by = c('maximo_grado_academico_id' = 'grado_academico_id')) %>%
  left_join(x =., y = categoria_conicet, by = 'categoria_conicet_id') %>%
  left_join(x = ., y = tipo_personal, by = 'tipo_personal_id') %>%
  left_join(x =., y = condicion_docente, by = 'tipo_condicion_docente_id') %>%
  left_join(x = ., y = disciplina, by = c('disciplina_experticia_id' = 'disciplina_id')) %>%
  left_join(x = ., y = disciplina, by = c('disciplina_maximo_grado_academico_id' = 'disciplina_id'), suffix = c('_maximo_grado_academico', '_maximo_grado_academico')) %>%
  left_join(x = ., y = disciplina, by = c('disciplina_titulo_grado_id' = 'disciplina_id'), suffix = c('_titulo_grado', '_titulo_grado')) %>%
  left_join(x = ., y = disciplina, by = c('disciplina_experticia_id' = 'disciplina_id'), suffix = c('_expertisia','_expertisia')) %>%
  left_join(x = ., y = disciplina, by = c('disciplina_titulo_grado_id' = 'disciplina_id'), suffix = c('_titulo_grado', '_titulo_grado'))

write_csv(indicadores_personas_ref,'indicadores_personas_referenciado.csv')
