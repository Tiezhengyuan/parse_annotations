# pAnnot: Term-based Parsing of genome annotations

## 1. Introduction
The bioinformatics tool pPAnnot could create on-site genome annotations and parse them with datasets.
The datasets could be read counts table determined by high-throughput sequence data.
The parsed datasets could be used for functional genomic study,
such as ontology enrichment, pathway enrichment, clustering, etc.

The tool pAnnot is very flexible because the parsed genome annotation is term-based. You migh as well consider
pAnnot if you face one of those issues as the following:
- You need some not widely supported genome annotations: For some mode organism namely human, many tools or R packages
    are available. In that case, you may not need pAnnot. But it is hard to collect genome annotations for many species
    though they may be recorded in public database.
- You need Non-geneme annotations: For some microbial or environmental study, tremendous data are not complete genome.
    Or those taxonomy is unknown.
- I have multiple reference genome annotations. That is possible in biomedical science. For large sequencing project
    on diferent population, different references are needed.
- Unpublished genome annotations. New hybrid plants in the plant science, or untaxonomy strains in microbiological studies
    would generate some genome annotations though such annotations may be computationally determined.

## 2. Testing and installation
The tool is developed and tested in Python3. Minimum hardware: 32GB RAM, 200GB hard drive space.

### 2.1. development



```
pip install -r requirements.txt
# do unit testing
pytest tests/unittests
# do local testing
pytest tests/localtests
```
Verify the environment variables defined in .env in the app directory.
Make sure the variables DIR_DOWNLOAD and DIR_CACHE are correctly defined.
In windows, 
```
set PYTHONPATH=%PYTHONPATH%;F:\parse_annotations
```

### 2.2. installation


```
git clone git@github.com:Tiezhengyuan/parse_annotations.git
cd parse_annotations
pip install .
```


## 3. Quick start


### steps:
        1.download source data from NCBI and ExPASy
        2.build local database 
        3.parse genome annotations

### example 1:  
Build human genome annotations. The major steps are showed as the below:
```
python pAnnot.py -s download
python pAnnot.py -s build -p human -t taxonomy 96606
python pAnnot.py -s map -p human -t GeneID
python pAnnot.py -s map -p human -t TranscriptID
python pAnnot.py -s map -p human -t UniProtKB
```
For Entrez Gene data, there are ~34 terms give a gene.
For UniProtKB, there are ~64 terms give a protein. In default, 
some 20-30 terms are selected for mapping. it is ok to include more terms with your needs.

For example, there is a data frame. genes are in rows and samples are in columns.
Each gene is identified by GeneID.
```
  id  sample_1  sample_2
0  1         4        14
1  2         5        25
2  3        78         8
```

I would like to add symbols for all genes. Run the codes showed as the following
```
from pAnnot.parser.parse import Parse

p = Parse(df)
p.declare_project('human')
# parse term GeneID ~ Symbol
p.parse_column('id', 'GeneID')
p.parse_term("Symbol")
p.add_parsing()
```

Here is the final dataframe after parsing. pAnnot would parse symbol 
column to the existing data frame.
```
  id  sample_1  sample_2 Symbol
0  1         4        14   A1BG
1  2         5        25    A2M
2  3        78         8  A2MP1
```

The parsing function of pAnnot is very powerful. We could build chromosome locus for all genes.
We could use pAnnot to build gene-positin table for UCSC Genome browser (https://genome.ucsc.edu/) or 
some genomic graphic software namely Circos (http://circos.ca/).
```
df = pd.DataFrame({
    'id': ["NM_000016.6", "NM_000023.4","NM_000224.3",\
        "NM_000265.7","NM_000257.4","NM_000726.5"],
    's1': [4,5,78,3,0,40],
    's2': [14,25,8,31,100,20],
})
c = Parse(df)
c.declare_project('human')
c.parse_column('id', 'RNA_nucleotide_accession.version')
c.parse_term("chromosome")
c.add_parsing()
c.parse_term("start_position_on_the_genomic_accession")
c.add_parsing()
c.parse_term("end_position_on_the_genomic_accession")
c.add_parsing()
```
Here is the result
```
            id chromosome    start_position_on_the_genomic_accession              end_position_on_the_genomic_accession
0  NM_000016.6          1               11430|75561368|4989|75724708                      50762|75600338|44321|75763678
1  NM_000023.4         17              193636|51033072|5000|50166004                     203559|51042984|14927|50175927
2  NM_000224.3         12          18681|52913413|5247|52948854|1960                  22732|52917464|9035|52952905|6011
3  NM_000265.7          7              210726|75976303|5047|74774010                     226140|75991630|20351|74789314
4  NM_000257.4         14  46750|17613743|328|5|14|114|23412739|4975  69671|17636657|445|123|190|160|103|109|148|122...
5  NM_000726.5          2                   152284204|151832770|5035                         152551128|152099166|271308
```


### example 2: 
Build cellulase-related annotations
```
python pAnnot.py -s download
python pAnnot.py -s build -t title cellulase
python pAnnot.py -s map -t "NCBI Accession Number"
```



## 4. references
-NCBI FTP: ftp.ncbi.nlm.nih.gov/gene/DATA/
-ExPASy FTP: ftp.expasy.org