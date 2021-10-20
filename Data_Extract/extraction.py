#Dependencies
import PyPDF2
import re
import pandas as pd
import numpy as np
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams
import random
import matplotlib.pyplot as plt
from nltk.tokenize import WordPunctTokenizer
from unidecode import unidecode
from itertools import compress
from itertools import combinations
from fuzzywuzzy import process, fuzz
import scrapy
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
##

#Importing functions
from SAN_parsing_fns import *
from SAN_scraping_fns import *
##

#Wrapper function to extract data from all the pdf files
def san_parser_wrapper():
    #Takes no arguments and returns a pandas data frame

    #General template to use when extracting the poster information from the pdf
    df_template = pd.DataFrame(columns = ['autor', 'tema', 'poster'])

    #Empty pandas data frame object to hold the extracted information for every pdf file
    final_df = df_template.copy()

    #Dictionary containing references to the different SAN meetings as keys and a list containing the range of pages that contain posters, the name of the parsing function for that year and the path to the pdf file
    san_posters = {
        'san_2019': [range(2,257), san_2019_parser, '../SAN_Books/SAN_2019.pdf'],
        'san_2018': [range(76,362), san_2018_parser, '../SAN_Books/SAN_2018.pdf'],
        'san_2017': [range(48,212), san_2017_parser, '../SAN_Books/SAN_2017.pdf'],
        'san_2015': [range(94,100), san_2015_parser, '../SAN_Books/SAN_2015.pdf'],
        'san_2014': [range(45,192), san_2014_parser, '../SAN_Books/SAN_2014.pdf'],
        'san_2013': [range(113,341), san_2013_parser, '../SAN_Books/SAN_2013.pdf'],
        'san_2012': [range(42,249), san_2012_parser, '../SAN_Books/SAN_2012.pdf']
    }

    #Regex pattern to detect the poster title
    titulo_regex = re.compile(r'P(\d)+.-')

    #First poster topic in the 2014 file to use with the 2014 parsing function
    tema_2014 = 'Cellular and Molecular Neurobiology'

    #Loads the science and technology staff dataset and gest the names that have a frequency higher than 150.
    personas = pd.read_csv('../CyT_Datasets/personas.csv', sep = ';', low_memory = False,
                      encoding='UTF-8')
    personas_na = personas[personas['nombre'].notna()]
    nombres_personas = personas_na['nombre'].map(unidecode).str.lower().str.split(expand=True).stack().value_counts()
    nombres_personas = nombres_personas[nombres_personas >= 150]

    #Loop over all the dictionary keys
    for i in san_posters.keys():
        #Assign a copy of the template data frame to hold the results from the current iteration 
        temporary_df = df_template.copy()
        #If the current iteration is the 2017 file then allow for different parsing logic
        if i == 'san_2017':
            #Open and read the corresponding pdf file
            san_2017_pdf = open(san_posters[i][2], 'rb')
            #Construct the reader object with the pdf file previously opened
            san_2017_reader = PyPDF2.PdfFileReader(san_2017_pdf)
            #Loop as always over the range of pages
            for p in san_posters[i][0]:
                #First parsing method
                parseo_1 = san_2017_reader.getPage(p).extractText()
                #Second parsing method.
                parseo_2 = extract_text(san_posters[i][2], page_numbers=[p])
                #Concatenate the data frame object obtained from this iteration with the, at first, empty template data frame (temporary_df)
                temporary_df = pd.concat(
                [
                    temporary_df,
                    san_posters[i][1](parseo_1, parseo_2)
                ]
                )
        #Whenever the current iteration is not 2017, follow a standard logic
        else:
            #Loop over the range of pages
            for p in san_posters[i][0]:
                #Concatenate the data frame object obtained from this iteration with the, at first, empty template data frame (temporary_df)
                temporary_df = pd.concat(
                    [
                    temporary_df, san_posters[i][1](extract_text(san_posters[i][2], page_numbers = [p]))
                    ]
                )
        #Reset the index of the pandas data frame object holding the results from the parsing process for the current iteration
        temporary_df = temporary_df.reset_index()

        #If the current iteration is the 2012 file execute a fix of the parsed data
        if i == 'san_2012':
            temporary_df = san_2012_fix(temporary_df)

        #Add a year column to identify the year of the data frame
        temporary_df['year'] = re.compile(r'\d+').search(str(i)).group()
        
        #Save the results from the current iteration as a csv file
        temporary_df.to_csv('../SAN_csv/' + i + '.csv')

        #Concatenate the results from the current iteration with the, at first, empty data frame assigned at the beginning of the function
        final_df = pd.concat(
            [final_df,
            temporary_df]
        )
    #Save the final data frame as a csv file
    final_df.to_csv('../SAN_csv/all_parsed_data.csv')

    #Output data frame containing all the parsed results
    return final_df


#Scraping function for the 2020 SAN Meeting
def san_scraper_wrapper():
    #Takes no arguments and returns a pandas data frame

    #Generate an empty pandas dataframe to hold the results from the scraping process
    df_autores = pd.DataFrame(columns = ['autor', 'afiliacion', 'poster','tema', 'primer_autor'])
    #2020 Meeting URL which holds all the posters
    san2020 = r'https://san2020.saneurociencias.org.ar/epostersbytopics/'
    #Driver (browser) startup
    driver = webdriver.Firefox()
    #Redirect the driver to the 2020 Meeting URL
    driver.get(san2020)
    #Generate the scrapy Selector object using the source code from the website
    san_sel = scrapy.Selector(text=driver.page_source)
    #Lista con todas las url que contiene la pagina relativas a los posters
    todos_url = san_sel.xpath('//div[@class="elementor-row"]//a/@href').extract()

    #Iteracion por cada url de la lista
    for u in todos_url:
        #Chequeo de que se trate de una url a un poster
        if 'san2020.saneurociencias.org.ar/posters/' in u:    
            #Redireccion del driver a la pagina del poster
            driver.get(u)
            #Generacion del Selector scrapy con el codigo de la pagina del poster
            poster_sel = scrapy.Selector(text = driver.page_source)
            #Extraccion del titulo del poster
            titulo_poster = poster_sel.xpath('//title/text()').extract()[0]
                #Remocion de elementos superfluos del titulo del poster
            titulo_poster = titulo_poster.replace('– SAN2020','').strip()
            #Extraccion del tema del poster 
            tema_poster = poster_sel.xpath('//div[@class="elementor-element elementor-element-d3567ab elementor-column elementor-col-50 elementor-top-column"]//h2[@class="elementor-heading-title elementor-size-default"]/a[@rel="tag"]/text()').extract()[0]
                #Chequeo de correcta extraccion del tema del poster usando otro metodo alternativo de extraccion
            if tema_poster == poster_sel.xpath('//h2[@class="elementor-heading-title elementor-size-default"]/a[@rel="tag"]/text()').extract()[1]:
                print('Extraccion de tema OK.')
            else:
                print(f'Inconsistencias en la extraccion del tema para poster:\n{titulo_poster}')
            #Extraccion de los autores y las afiliaciones
            autores_afil = extraccion_autores(poster_sel)
            #La primera lista contiene los autores y la segunda las afiliaciones
            autores,afiliaciones = autores_afil[0], autores_afil[1]
            #Dataframe con los nombres de los autores y los nombres de las afiliaciones
            aut_afil = extraccion_afiliaciones(poster_sel, autores, afiliaciones)
                #Agregado de columna con el titulo y el tema del poster
            aut_afil['poster'] = titulo_poster
            aut_afil['tema'] = tema_poster
                #Agregado de columna para definir si es el primer autor
                    #False para todos los autores menos el primero
            primer_autor = [False] * (len(autores) - 1)
                    #Agrego True para el primer autor
            primer_autor = primer_autor.insert(0, True)
                    #Agrego la lista a la columna de primer autor
            aut_afil['primer_autor'] = primer_autor
            #Agregado de los resultados al dataframe de autores final
            df_autores = df_autores.append(
                aut_afil
            )

    #Extraccion de los IDs de los topicos de los posters
    topics_id = san_sel.xpath('//div[@class="elementor-text-editor elementor-clearfix"]/p/a/@href').extract()

    #Extraccion de los nombres correspondientes a cada ID de los topicos de los posters
    topics_name = san_sel.xpath('//div[@class="elementor-text-editor elementor-clearfix"]/p/a/text()').extract()

    #Remocion del # de cada string de la lista
    topics_id = [top.replace('#','') for top in topics_id]

    #Creacion de diccionario con los topics id como key y los nombres del topic como value
    topic_dic = {}
    for i in range(len(topics_id)):
        topic_dic[topics_id[i]] = topics_name[i]

    #Save the results as a csv file
    df_autores.to_csv('../SAN_csv/SAN_2020_autores.csv')

    #Output data frame object containig the results from the scraping process
    return df_autores

def extraction_wrapper():

    #Call for the pdf parsing wrapper function
    final_parsing = san_parser_wrapper()

    #Call for the web scraping wrapper function
    final_scraping = san_scraper_wrapper()

    #Select only the 4 relevant columns of the dataframe
    final_parsing = final_parsing[
        ['autor','tema','poster', 'year']
    ]
    final_scraping = final_scraping[
        ['autor','tema','poster', 'year']
    ]
    #Merge the two data frames together
    final_san_df = pd.concat(
    [final_parsing, final_scraping]
    )

    #Save the results as a csv file
    final_san_df.to_csv('../SAN_csv/all_posters.csv')

    #Output data frame object that contains all the posters
    return final_san_df

extraction_wrapper()