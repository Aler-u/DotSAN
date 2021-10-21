# DotSAN (Dataset of the Argentine Society for Neuroscience)

DotSAN is a project to map the names of all Argentinian neuroscientists and link them with various public data sources to create a comprehensive picture of the Argentinian neuroscience research landscape that may serve multiple purposes including, but not limited to, evidence-based policy and institutional decisions as well as scientific production upon the structure and dynamics of such community. 

Given the fact that there isn't a clear-cut category within the Argentine scientific system to distinguish neuroscientists and given the particular nature of the discipline (such as the strong interdisciplinarity) we believe it is important to come up with adequate data to characterize this community. 

## What does the repository contain?

There are 6 folders in this repository. The *Data_Extract* folder contains the code to extract and merges all the poster data from the pdf files and the 2020 website and stores it as .csv files in the *SAN_csv* folder which already contains the extracted information. The *Data_PreProcessing* folder contains the code to perform the fuzzy name matching and the RMarkdown file exploring the development of the threshold criteria used in the analysis shown in the *SAN_2021_Presentation* RMarkdown file inside the *Analysis* folder.

## General Use

The file *all_posters.csv* within the *SAN_csv* folder contains the poster information for all the pdf files plus the 2020 website while the *matche_nombres.csv* contains the matchs for the author names based on the fuzy name matching algorithm. The *matche_nombres.csv* allows join operations with the datasets inside the *CyT_Datasets* folder which contains all the datasets from the SICYTAR. 

If you just want the extracted and curated data to use right away, then there are two main ways to proceed. 

The easisest way is to clone the current repository into your local machine by executing the following command   
`git clone https://github.com/Aler-u/DotSAN.git`  
From there you get all the files included in the repository so you can use whatever file you need. 

The second way is to download a .zip file containing all the files directly from this github repository and then proceed the same as before. 

A third way, albeit more complicated, is to navigate inside the repository towards the .csv file you want, open it and click the _Raw_ option which will open a new tab from where you now can save the page as a plain text file.

## Collaboration

We encourage active collaboration, particularly from the neuroscience community. We believe this project serves a community purpose and is thus a collective effort.

You can collaborate by reporting issues or helping with more features and assets. 

## Future Steps

* Train an algorithm with the public data from the SICYTAR to detect author names, poster titles and affiliations in a file-independent manner.  
* Create an interactive graph from the co-authorship network 
* Integrate other data sources such as ORCID or ResearchGate

## LICENSE

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

