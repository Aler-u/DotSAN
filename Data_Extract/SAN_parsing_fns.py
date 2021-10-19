#The file contains all the functions used to extract data from the various pdf files contained in the 'SAN_Books' directory and a function to evaluate the performance of the extraction process for an individual file

## Parsing results evaluation function
def parser_performance(dataset, no_pages = None):
    #The function takes two arguments and prints a series of metrics for the current data frame.
        #dataset = expects a pandas data frame object
        #no_pages = expects a positive integer reflecting the number of pages examined by the parser (defaults to None)

    title_len = dataset['titulo'].dropna().str.len().values
    authors = dataset['autor'].dropna()
    authors = authors.apply(lambda x: unidecode(x))
    authors = authors.apply(lambda x: re.compile(r'[a-zA-Z\s]*').search(x).group())
    authors_len = authors.str.split(' ').apply(len).values
    print('\n','Authors names length','\n')
    plt.hist(authors_len)
    plt.show()
    print('\n','Poster title length','\n')
    plt.hist(title_len)
    plt.show()
    author_95 = np.percentile(authors_len, [5,95])
    title_95 = np.percentile(title_len, [5,95])
    print(
        '-'*50,
        'Authors',
        '\n',
        '5-95 percentiles:','\n',
          '5th: {percentil5}'.format(percentil5 = author_95[0]),' - ',
          '95th: {percentil95}'.format(percentil95 = author_95[1]),'\n',
         '5th count: {cuenta5}'.format(cuenta5 = np.sum(authors_len < author_95[0])),' - ',
         '95th count: {cuenta95}'.format(cuenta95 = np.sum(authors_len > author_95[1])),
        '\n',
         '-'*50,
        '\n',
          'Titles',
        '\n',
          '5-95 percentiles:',
        '\n',
          '5th: {percentil5}'.format(percentil5 = title_95[0]),' - ',
          '95th: {percentil95}'.format(percentil95 = title_95[1]),'\n',
         '5th count: {cuenta5}'.format(cuenta5 = np.sum(title_len < title_95[0])),' - ',
         '95th count: {cuenta95}'.format(cuenta95 = np.sum(title_len > title_95[1])),
        '\n',
         '-'*50,
        '\n',
            dataset['tema'].value_counts()
         )


## 2019 Parsing Function
def san_2019_parser(poster_string):
    #The function takes one argument and returns a pandas data frame object.
        #poster_string = expects a string from a parsed pdf file page        

    #Poster topic
    tema = poster_string.split('\n')[0]
    #Poster title
    titulo = compress(
            poster_string.split('\n\n'), 
            [titulo_regex.search(elements) != None for elements in poster_string.split('\n\n')]
    )
    #Poster authors
    autores = poster_string.split('\n \n')[2]
    #Data frame output
    return pd.DataFrame(
                {'autor': autores.split(','),
                'tema': tema,
                'poster': titulo}
                )

## 2018 Parsing Function
def san_2018_parser(poster_string):
    #The function takes one argument and returns a pandas data frame object.
        #poster_string = expects a string from a parsed pdf file page        

    #Poster topic
    tema = poster_string.split('\n\n')[0]

    #Poster title
    titulo = compress(
            poster_string.split('\n\n'), 
            [titulo_regex.search(elements) != None for elements in poster_string.split('\n\n')]
    )
    #Poster authors
    autores = poster_string.split('\n\n')[[titulo_regex.search(elements) != None for elements in poster_string.split('\n\n')]].split('\n \n')[0]
    #Data frame output
    return pd.DataFrame(
                {'autor': autores.split(','),
                'tema': tema,
                'poster': titulo}
                )

## 2017 Parsing Function
def san_2017_parser(poster_str, poster_str2):
    #The function takes two arguments and returns a pandas data frame object.
        #poster_str = expects a string from a parsed pdf file page following pdfminer method
        #poster_str2 = expects a string from a parsed pdf file page following PyPDF2 method

    #List holding poster elements 
    poster_spliteado = poster_str.split('  ')
    #Poster topic
    tema = poster_spliteado[1].strip()
    #Poster title
    titulo = poster_spliteado[2]
    #List holding poster authors
    autores = poster_str2.split('\n \n')[2].split(',')
    #Data frame output
    return pd.DataFrame(
                    {'autor': autores,
                    'poster': titulo,
                    'tema': tema}
                    )

## 2015 Parsing Function
def san_2015_parser(poster_string):
    #The function takes one argument and returns a pandas data frame object.
        #poster_string = expects a string from a parsed pdf file page  
    
    #Poster topic
    tema = poster_string.split('\n \n')[1]
    #Poster title
    titulo = poster_string.split('\n \n')[2]
    titulo = ''.join(titulo.splitlines())
    #Poster authors
    autores = poster_string.split('\n \n')[3]
    elementos = autores.split('\n')
        #Poster authors extraction
    primer_elemento = elementos[0]
    try:
        segundo_elemento = elementos[1]
    except:
        print(f'Error en pagina {i + 1}')
        return()
    if len(primer_elemento) > 85:
        if 'Laboratorio' in segundo_elemento or 'Instituto' in segundo_elemento or 'CONICET' in segundo_elemento:
            autores = primer_elemento.split(',')
        else:            
            autores = ''.join(autores.split('\n')[0:2]).split(',')
    else:
        autores = primer_elemento.split(',')
    #Data frame output
    return pd.DataFrame(
                        {'autor': [autor.strip() for autor in autores],
                        'poster': titulo,
                        'tema': tema}
                        )

## 2014 Parsing Function
def san_2014_parser(poster_string):
    #The function takes one argument and returns a pandas data frame object.
        #poster_string = expects a string from a parsed pdf file page  

    #Regex pattern to detect authors element
    autores_regex = re.compile(r'(\S*\s\S*),')
    #Empty dataframe to hold output
    res_df = pd.DataFrame({'autor': [], 'poster': [], 'tema':[]})
    #String split by newlines
    string_separada = poster_string.split('\n')
    #Conditional over the status of the first element (poster or title)
    if titulo_regex.search(string_separada[0]) == None:
        #If true, first element is poster topic
        global tema_2014 #Assign as global variable to use in the next function call
        tema_2014 = string_separada[0]
        titulo = string_separada[2]
        indice = 2
    else:
        #If false, first element is poster title
        titulo = string_separada[0]
        indice = 0
    #Conditional over next element status (poster title or authors) by regex result
    if len(autores_regex.findall(string_separada[indice + 1])) < 2:
        #If true, element is poster title
        titulo = titulo + ' ' + string_separada[indice + 1]
        autores = string_separada[indice + 2]
        indice = indice + 2
    else:
        #If false, element contains authors names
        autores = string_separada[indice + 1]
        indice = indice + 1
    #Conditional over next element status (authors or affiliations)
    if any(afil_key in string_separada[indice + 1] for afil_key in filiaciones_keywords_2014) or process.extractOne(query = string_separada[indice + 2], choices = filiaciones_keywords_2014, scorer = fuzz.partial_ratio)[1] > 85:
        #If true, element contains affiliations thus we ignore it
        pass
    else:
        #If false, element contains more author names
        autores = autores + string_separada[indice + 2]
    #Loop over each author name and add them to the final data frame
    for aut in autores.split(','):
        tmp_df = pd.DataFrame(
            {'autor': [aut], 'poster': [titulo], 'tema': [tema_2014]}
        )
        res_df = res_df.append(tmp_df)
    #Data frame output
    return(res_df)    

## 2013 Parsing Function
def san_2013_parser(poster_string):
    #The function takes one argument and returns a pandas data frame object.
        #poster_string = expects a string from a parsed pdf file page  

    #Topic
    tema = poster_string.split('\n')[0]
    #Title
    titulo = poster_string.split('\n \n')[1]
    #If the title has a lenght greater than 1000 it means the variable contains more elements than just the title
    if len(titulo) > 1000:
        #It may be the spliting parameter so we try a different newline combination
        titulo = poster_string.split('\n\n')[1]
        #If this newline also fails (given by a huge length) it may separation between the title and the poster/session
        if len(titulo) > 1000:
            #To solve it, we split with the poster/session element and select the last element
            #The poster/session element is the second element, splited by newlines, in the first element splited by two consecutive newlines
            titulo = poster_string.split('\n\n')[0].split(poster_string.split('\n\n')[0].split('\n')[1])[-1]
    #Empty string to held the authors names
    autores = ''
    #Divide the string by the title    
    potenciales_autores = poster_string.split(titulo)[1].split('\n') #Element containing the authors, afiliations and poster text
    #Index to start iterating in the first element of potenciales_autores
    a_i = 0
    #Continue until any word in the i element of potenciales_autores is in the list of filiaciones_keywords
    #Any element beyond the one who fullfils these requirements doesn't contain any authors and is not of interest
    while not any([p in filiaciones_keywords_2013 for p in potenciales_autores[a_i].split(' ')]):
        print(a_i)
        #Break the loop if it reaches a long underscore line which indicates the beginning of the poster text
        if "_" in potenciales_autores[a_i]:
            #If the loop reaches this conditional it means it failed to detect afiliations, thus display a warning
            print('ERROR! No se detectaron filiaciones')
            break
        #Add authors to the autores list variable only if the i element has a length greater than 2
        #This is done to avoid elements like ' ' to be added
        elif len(potenciales_autores[a_i].strip()) > 2:
            autores = autores + potenciales_autores[a_i]
        else:
        #Skip the element if above conditions are not met
            pass
        #Move on to the next element
        a_i += 1 
    #Split authors by commas to get one author per element in a list
    autores = autores.split(',')
    #Data frame output
    return pd.DataFrame(
            {'tema': [tema], 
             'poster': [titulo], 
             'autor': [autores]}
    )                     

## 2012 Parsing Function
def san_2012_parser(poster_string):
    #The function takes one argument and returns a pandas data frame object.
        #poster_string = expects a string from a parsed pdf file page  

    #List with poster elements, split by newline 
    poster_split = poster_string.split('\n')
    #Poster topic
    tema = poster_split[2] 
    #Poster title
    t_i = 0
    try:
        while 'poster number' not in poster_split[t_i].lower(): #Search elements by index until reference words are found
            t_i += 1 #Go to the next element
    except:
        return
    #t_i contains the poster and session reference
    #The title starts at t_i + 1
    t_i += 1
    #Empty title string
    titulo = ''
    #Any element lacking a comma and a name is considered part of the title
    while ',' not in poster_split[t_i] and not any([x in unidecode(poster_split[t_i].lower()) for x in nombres_personas.keys()]): 
        titulo = titulo + poster_split[t_i] #Add the element to the title
        t_i += 1 #Go to the next element
    #The authors start at the t_i + 1 element
    a_i = t_i + 1
    #Empty authors string 
    autores = ''
    #If there is no match for the afilitations keywords then we assume the element contains authors names
    while not any([p in poster_split[a_i].lower() for p in filiaciones_keywords_2012]):
        #Add the element to the authors string
        autores = autores + poster_split[a_i]
        a_i += 1 #Move to the next element
        #Check that the loop doesn't reach an element containing an 'at sign'
        if '@' in poster_split[a_i]:
            #If True
            #Display an error message with the number of the page
            print(f'ERROR! in {t_i}, page number {i}')
            #Add the ERROR string to the authors strings to facilitate detection of failed pages
            autores = autores + 'ERROR'
            #Break the loop to avoid looping over other non-useful elements
            break
    #Data frame output
    return pd.DataFrame({'tema': tema, 'autor': autores.split(','), 'poster': titulo})

## 2012 Final data frame fix function
def san_2012_fix(df_2012):
    #The function takes one argument and returns a pandas data frame object
        #df_2012 = expects a pandas data frame object from the output of the 2012 parsing function

    #Drop erronous rows
    df_2012 = df_2012.drop([36,380])
    #Manually add correct information
    df_2012 = pd.concat(
        [df_2012, pd.DataFrame({'tema': 'Cellular and Molecular Neurobiology', 'autor': ['Victor Danelon', 
                                                                                'Andrea B. Cragnolini', 
                                                                                'Daniel H. Masco'],
                      'titulo': "An in vitro model of SE induces neuronal death and changes in the levels of TrkB, pTrkB and p75ntr receptors in a mixed culture of neurons and astrocytes"})]
        )
    df_2012 = pd.concat(
        [df_2012, pd.DataFrame({'tema': ['Computational Neuroscience'], 'autor': ['Juan Pablo Oliver'],
                                   'titulo': ['Active mapping of brain']})]
        )
    #Reset index and drop redundant columns
    df_2012 = df_2012.reset_index().drop(['level_0','index'], axis = 1)
    #Data frame output
    return df_2012

