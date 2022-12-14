# Brasil run off Ballot Data (Boletin the Urna) - 2022

What motivated me to download all Ballot Data (Boletin the Urna - BU) is the controversy about the legitimacy of the election results.

I am making available all the ballot data (BU) files and data that I could download so far.

It was downloaded from the TSE website [resultados.tse.jus.br](resultados.tse.jus.br)

Python programming language was used to download and analyze the data and I made it available in a PUBLIC FOLDER folder that I made public to anyone.

So you do not need to download the files yourself. Took me a few days. In beginning I was using thread to download but I was getting a rate of 4 BUs per second. Later I developed a new scrip that download asynchronously with a rate of about 20 BUs + per second. I would not recommend to use a too high rate not to reach rate limit and get your ip blocked to make requests to tse server. 

Se the asynchronous script `async_get_ballot_bu.py` for more information. 

There is a total of 472.075 ballots in this election I downloaded.

According to the TSE site there are [472.075](https://www.tse.jus.br/comunicacao/noticias/2022/Outubro/eleitores-comecam-a-votar-nas-mais-de-472-mil-secoes-eleitorais-espalhadas-pelo-brasil) section (ballots) 

To have access to the data downloaded you can access in this [container](https://storage4223.blob.core.windows.net/bu-elections-2022)

There are 95 ballots I was not able to decode. found in `bu_not_able_decode.csv`

## Analysis

There was a brief analysis I have done with the data in Jupyter notebook.

see `notebook` folder.

I could find 141 ballot with zero votes for Bolsonaro and 4 with zero votes for Lula.

Also there is a .csv version where you can load in excel if you are not familiar with python.

`total_votes_president.csv`

If anyone with statistic knowledge who wants to analyze the data more thoroughly please feel free.

## TSE technical documentation

The analysis and the gathering of this data was only possible because I found a documentation on how to decode and read the BU data which can be
found [here](https://www.tre-mt.jus.br/eleicoes/eleicoes-2022/documentacao-tecnica-do-software-da-urna-eletronica)

## Disclaimer

This analysis has no intention to cast doubt in the process and the legibility of the election. The intend is just to bring transparency and for people to have access to the data at a more granular level to make sure no distortion and non factual data is misleading people. 