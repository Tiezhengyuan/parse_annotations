# pAnnot: Term-based Parsing of genome annotations

## 1. Introduction
The bioinformatics tool pPAnnot could create on-site genome annotations and parse them with datasets.
The datasets could be read counts table determined by high-throughput sequence data.
The parsed datasets could be used for functional genomic study,
such as ontology enrichment, pathway enrichment, clustering, etc.

The tool pAnnot is very flexible because the parsed genome annotation is term-based. You migh as well consider
pAnnot if you face one of those issues as the following:
    - You need some not widely supported genome annotations: For some mode organism namely human, many tools or R packages
        are available. but it is hard to collect genome annotations for many species though they may be recorded
        in public database.
    - You need Non-geneme annotations: For some microbial or environmental study, tremendous data are not complete genome.
        Or those taxonomy is unknown.
    - I have multiple reference genome annotations. That is possible in biomedical science. For large sequencing project
        on diferent population, different references are needed.
    - Unpublished genome annotations. New hybrid plants in the plant science, or untaxonomy strains in microbiological studies
        would generate some genome annotations though such annotations may be computationally determined.

## 2. Testing and installation
The tool is developed and tested in Python3. Minimum hardware: 32GB RAM, 200GB hard drive space.

### 2.1. unit test

```
pip install -r requirements.txt
pytest tests/unittests
```

### 2.2. local test

```
pytest tests/localtests
```

### 2.3. installation


```
python setup.py
```
Verify the environment variables defined in .env in the app directory.
Make sure the variables DIR_DOWNLOAD and DIR_CACHE are correctly defined.


## 3. Quick start


### steps:
        1.download source data from NCBI and ExPASy
        2.build local database 
        3.parse genome annotations
### example 1:  
Build human genome annotations
```
python pAnnot.py -s download
python pAnnot.py -s build -t taxonomy 96606
python pAnnot.py -s parse -t "NCBI Accession Number"
```

### example 2: 
Build cellulase-related annotations
```
python pAnnot.py -s download
python pAnnot.py -s build -t title cellulase
python pAnnot.py -s parse -t "NCBI Accession Number"
```



## 4. references
NCBI FTP: ftp.ncbi.nlm.nih.gov/gene/DATA/
ExPASy FTP: ftp.expasy.org