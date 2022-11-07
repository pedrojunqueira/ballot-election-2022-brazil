# Brasil run off Ballot Data (Boletin the Urna) - 2022

What motivated me to download all Ballot Data (Boletin the Urna - BU) is the controversy about the legitimacy of the election results.

What is out there is certainly a lot of fake new.

What I will make available are all the ballot data (BU).

It was downloaded from the TSE website [resultados.tse.jus.br](resultados.tse.jus.br)

Python programming language was used to download and analyze the data and I made it available in a PUBLIC FOLDER folder that I made public to anyone.

So you do not need to download the files it self. Took me a few days. In beginning I was using thread to download but I was getting a rate of 4 BUs per second. Later I developed a new scrip that download asynchronously with a rate of about 20 BUs per second. 

There is a total of 464,401 in this election including 28 localities.

To have access to the data you can access in this folder


## TSE technical documentation

The analysis and the gathering of this data was only possible because I found a documentation on how to decode and read the BU data which can be
found [here](https://www.tre-mt.jus.br/eleicoes/eleicoes-2022/documentacao-tecnica-do-software-da-urna-eletronica)