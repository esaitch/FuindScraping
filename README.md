# Funding research - scraping project

### Included funders
| Funder                            | Scraping possible | Completed | Output                                                                                                    |
|-----------------------------------|-------------------|-----------|-----------------------------------------------------------------------------------------------------------|
| Independent Research Fund Denmark |         y         |     y     |   [dff](https://github.com/esaitch/FundScraping/blob/master/funds/outputs/dff_output.json "dff output")   |
| Danish National Research Foundation |       ?         |            |                      |
| Novo Nordisk Foundation           |         y         |     y     |   [novo](https://github.com/esaitch/FundScraping/blob/master/funds/outputs/novo_output.json), [novo2](https://github.com/esaitch/FundScraping/blob/master/funds/outputs/novo2_output.json)                                                                                                       |
| Lundbeck Foundation               |         y         |     y     |   [postdocs](https://github.com/esaitch/FundScraping/blob/master/funds/outputs/lundbeckpostdocs_output.json) [all](https://github.com/esaitch/FundScraping/blob/master/funds/outputs/lundbeckall_output.json)        |
| Helsefonden                       |         y         |     y     |   [Helsefonden](https://github.com/esaitch/FundScraping/blob/master/funds/outputs/helsefonden_output.json)   
| Villum Foundation                 | same as velux?    |           |   
| Carlsberg Foundation              |         y         |     y     |   [carlsberg](https://github.com/esaitch/FundScraping/blob/master/funds/outputs/carlsberg_output.json "dff output")   |
| Danish Cancer Society             |         ?         |           |      
| Velux Foundation                  |                   |     y     |   [Velux](https://github.com/esaitch/FundScraping/blob/master/funds/outputs/velux_output.json)                                                                                                        |
| Danish Ministry for Science and Technology|           |           |
| Tryg Foundation                   |                   |           |                                                                                                           |
| Nordea Foundation                 |                   |           |                                                                                                           |
| Innovation Fund Denmark           |                   |           |


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