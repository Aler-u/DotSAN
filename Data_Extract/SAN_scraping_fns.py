#The file contains all the functions used to extract data from the 2020 Annual Meeting website

def extraccion_autores(scrapy_sel):
    #Takes one argument and returns a list
        #scrapy_sel = expects a scrapy Selector Object

    #Empty list to hold clean authors names
    nueva_lista_autores = []
    #Empty list to hold afiliation numbers for each author
    lista_afiliaciones = []
    #Scrapy Selector object containing authors names
    autores_sel = scrapy_sel.xpath('//ul[@class="elementor-icon-list-items elementor-inline-items"]')[1]
    #Authors names extraction as a list
    autores_lst = autores_sel.xpath('*//span/text()').extract()
    #Generate a regex pattern to extract names and affiliations
    nombre_autor = re.compile('\D*[^¹²³⁴⁵⁶⁷⁸⁹𝄒1-9]')
    num_afiliacion = re.compile('[¹²³⁴⁵⁶⁷⁸⁹]')
    #Loop over each author name as they appear on the website
    for a_i in range(len(autores_lst)):
        #Matchs for the author name
        match_nombre = nombre_autor.findall(autores_lst[a_i])
        #Match for the affiliation
        match_afil = num_afiliacion.findall(autores_lst[a_i])
        #Check that the regex hasn't found more than one element (i.e. one name)
        if len(match_nombre) > 1:
            print(f'Error en {match_nombre}')
            break
        #Remove superscript numbers
        nombre_sin_num = match_nombre[0].strip()
        #Remove commas
        nombre_sin_coma = nombre_sin_num.replace(',','')
        #Remove whitespaces
        nombre_sin_w = nombre_sin_coma.strip()
        #Append the clean name
        nueva_lista_autores.append(nombre_sin_w)
        #Append the affiliation
        lista_afiliaciones.append(match_afil)
    #Output list
    return([nueva_lista_autores, lista_afiliaciones])

def extraccion_afiliaciones(scrapy_sel, aut, afil):
    #Takes two arguments and returns a pandas data frame object
        #scrapy_sel = expects a scrapy Selector object
        #aut = expects a list (of authors)
        #afil = expects a list (of affiliations)

    #Extraction of the institutions that make up the affiliations
    afil_lst = scrapy_sel.xpath('//ul[@class="elementor-icon-list-items"]//span/text()').extract()
    #Regex generation to separate the numbers from the name of the institution
    afil_num = re.compile('\d')
    afil_name = re.compile('\D+')
    #Dictionary to store the relationship between the number and the affiliation
    afil_dic = {}
    #Loop over each extracted affiliation
    for a_f in afil_lst:
        #Assign the affiliation number as the key in the dictionary and the name as the value
        afil_dic[int(afil_num.search(a_f).group())] = afil_name.search(a_f).group()
    #Data frame, each row contains the author and the affiliation
    df_autor_y_afil = pd.DataFrame(
    data = {'autor':aut, 
            'afiliacion': afil}
            )
    #Transform the superscript to integer by going from list to str and employing the str as the key to get the value from the dictionary 
    df_autor_y_afil['afiliacion'] = df_autor_y_afil['afiliacion'].apply(lambda x: afil_fun(x, afil_dic))
    #Ouput data frame 
    return(df_autor_y_afil)

def afil_fun(row, afil_dic):
    #Takes two arguments and returns a string or a list depending on the length input
        #row = expects a list
        #afil_dic = expects a dictionary holding the relationship between the number and the affiliation 

    #Check if the length of the list is higher than one
    if len(row) > 1:
        res_lng = []
        #Loop over every value to reeplace the reference number with the institution name
        for af in row:
            #Transform the numeric character superscript to an integer
            super_to_num = superscript_dic[af]
            #Get the name of the institution using the reference number
            afil_ref = afil_dic[super_to_num]
            #Append the result to the empy list
            res_lng.append(afil_ref)
        #Output list
        return(res_lng)
    else:
        #Transform the numeric character superscript to an integer
        super_to_num = superscript_dic[row[0]]
        #Get the name of the institution using the reference number
        res_sht = afil_dic[super_to_num]
        #Output string
        return(res_sht)