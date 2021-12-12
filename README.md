# Funding research - scraping project

### Status and information
Status of all crawlings along with a description of how they were made (including links and info about any decisions made underway) can be found in the following Google Docs:
https://docs.google.com/document/d/1uk9iTS6hwWHuyuGPU33GsPvmOlstQg-mbvPtjcLuW7w/edit#heading=h.5xb9zdipqj95 

### Included funders
| Funder                            | Scraping possible | Completed | Email         | Output                                                                                                    |
|-----------------------------------|-------------------|-----------|---------------|-----------------------------------------------------------------------------------------------------------|
| Independent Research Fund Denmark |         y         |     y     |      n        | [dff](https://github.com/esaitch/FundScraping/blob/master/funds/outputs/dff_output.json "dff output")   |
| Danish National Research Foundation |       y         |     y     |      y        | [dnrf](https://github.com/esaitch/FundScraping/blob/master/funds/outputs/dnrf_output.json)|
| Novo Nordisk Foundation           |         y         |     y     |      n        | [novoall](https://github.com/esaitch/FundScraping/blob/master/funds/outputs/novoall_output.json), [novocovid](https://github.com/esaitch/FundScraping/blob/master/funds/outputs/novocovid_output.json), [novoarticle](https://github.com/esaitch/FundScraping/blob/master/funds/outputs/novoarticle_output.json)                                                                                                       |
| Lundbeck Foundation               |         y         |     y     |      n        | [postdocs](https://github.com/esaitch/FundScraping/blob/master/funds/outputs/lundbeckpostdocs_output.json), [lundbeckall](https://github.com/esaitch/FundScraping/blob/master/funds/outputs/lundbeckall_output.json)        |
| Helsefonden                       |         y         |     y     |      n        | [helsefonden](https://github.com/esaitch/FundScraping/blob/master/funds/outputs/helsefonden_output.json)   
| Villum Foundation                 |         y         |     y     |      n        | [veluxvillum](https://github.com/esaitch/FundScraping/blob/master/funds/outputs/veluxvillum_output.json)  
| Carlsberg Foundation              |         y         |     y     |      n        | [carlsberg](https://github.com/esaitch/FundScraping/blob/master/funds/outputs/carlsberg_output.json)   |
| Danish Cancer Society             |         y         |     y     |      n        | [cancersociety](https://github.com/esaitch/FundScraping/blob/master/funds/outputs/cancersociety_output.json), [cancersociety_manual](https://github.com/esaitch/FundScraping/blob/master/funds/outputs/cancersociety_manual_output.json)     
| Velux Foundation                  |         y         |     y     |      n        | [veluxcovid](https://github.com/esaitch/FundScraping/blob/master/funds/outputs/veluxcovid_output.json)                                                                                                        |
| Danish Ministry for Science and Technology| y         |     y     |      n        | [ufm](https://github.com/esaitch/FundScraping/blob/master/funds/outputs/ufm_output.json) 
| Tryg Foundation                   |         y         |     y     |      n        | [tryg](https://github.com/esaitch/FundScraping/blob/master/funds/outputs/tryg_output.json)                                                                                                          |
| Nordea Foundation                 |         y         |     y     |               | [nordea](https://github.com/esaitch/FundScraping/blob/master/funds/outputs/nordea_output.json)                                                                                                         |
| Innovation Fund Denmark           |         y         |     y     |      n        | [innovationsfonden](https://github.com/esaitch/FundScraping/blob/master/funds/outputs/innovationsfonden_output.json), [innovationsfondencovid](https://github.com/esaitch/FundScraping/blob/master/funds/outputs/innovationsfondencovid_output.json)
| Region Sjælland                   |         y         |     y     |      n        | [regionsjaelland](https://github.com/esaitch/FundScraping/blob/master/funds/outputs/regionsjaelland_output.json)
| Region Hovedstaden                |         y         |     y     |      n        | [regionhovedstaden](https://github.com/esaitch/FundScraping/blob/master/funds/outputs/regionhovedstaden_output.json)
| Danish Heart Association          |         n         |     y     |      n        | [hjerteforeningen](https://github.com/esaitch/FundScraping/blob/master/funds/outputs/hjerteforeningen_output.json)
| Danish Rheumatism Association     |         y         |     y     |      n        | [gigtforeningen](https://github.com/esaitch/FundScraping/blob/master/funds/outputs/gigtforeningen_output.json)
| Elsass Foundation                 |         n         |     y     |      n        | [elsass](https://github.com/esaitch/FundScraping/blob/master/funds/outputs/elsass_output.json)
| Poul Due Jensen’s Foundation      |         n         |     y     |               | [pdjf](https://github.com/esaitch/FundScraping/blob/master/funds/outputs/pdjf_output.json)
| Augustinus Foundation             |         y         |     y     |      n        | [augustinusfonden](https://github.com/esaitch/FundScraping/blob/master/funds/outputs/augustinusfonden_output.json)
| Danish Energy Association         |         y         |     y     |      m?       | [energistyrelsen](https://github.com/esaitch/FundScraping/blob/master/funds/outputs/energistyrelsen_output.json)
| Advokat Bent Thorberg’s Foundation|         ?         |     ?     |               |
| Danish Energy Agency              |         ?         |     ?     |               |
| Gangsted Foundation               |         n         |     y     |      n        | [gangstedfonden](https://github.com/esaitch/FundScraping/blob/master/funds/outputs/gangstedfonden_output.json)
| Danish Horticulture               |         ?         |     ?     |               |
| Danish Sugar Beet Growers         |         n         |     y     |      n        | [sukkerroeafgiftsfonden](https://github.com/esaitch/FundScraping/blob/master/funds/outputs/sukkerroeafgiftsfonden_output.json)



### Outcome variables
| Variable                          | Description                                  |
|-----------------------------------|----------------------------------------------|
| id                                | A unique number                              |
| pi                                | Name of primary applicant                    |
| co_pi                             | Name of co-applicant(s)                      |
| pi_affiliation                    | Affiliation of primary applicant             |
| co_pi_affiliation                 | Affiliation of co-applicant(s)               |
| gender                            | Gender; male/female/other                    |
| career_stage                      | Career stage of primary applicant            |
| country_of_origin                 | Country of origin for primary applicant      |
| funder                            | Name of fund                                 |
| grant_programme                   | Name of grant programme                      |
| title                             | Title of research project                    |
| summary                           | Summary of research project                  |
| award_application_date            | Date of application or when fund was granted |
| start_date                        | Project start date                           |
| end_date                          | Project end date                             |
| amount_awarded                    | Amount of funding received                   |
| research_area                     | Research area                                |
| project_link                      | Link to project                              |
| funded                            | Funding received; 1/0 (yes/no)               |
| amount_sought                     | Amount applied for                           |
| review_score                      | Review score                                 |
| covid_specific                    | Covid specific research; 1/0 (yes/no)        |