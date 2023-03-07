identifiers = [
    # NCBI
    {
        'name': "NCBI taxonomy",
        'key': 'tax_id',
        'comment': 'taxonomy',
        'http': 'https://www.ncbi.nlm.nih.gov/taxonomy',
        'example': '654924',
    },
    {
        'name': "PubMed ID",
        'key': 'pmid',
        'comment': 'protein',
        'http': 'https://pubmed.ncbi.nlm.nih.gov',
        'example': '15165820',
    },
    {
        'name': "EntrezGene ID",
        'key': 'gene_id',
        'comment': 'DNA',
        'http': 'https://www.ncbi.nlm.nih.gov/gene',
        'example': '2947773',
    },
    {
        'name': "NCBI Model RefSeq",
        'key': 'refseq_acc',
        'comment': 'NCBI Reference Sequence',
        'http': 'https://www.ncbi.nlm.nih.gov/protein',
        'example': 'YP_031579.1',
    },
    {
        'name': "NCBI Known RefSeq",
        'key': 'refseq_acc',
        'comment': 'NCBI Reference Sequence',
        'http': 'https://www.ncbi.nlm.nih.gov/nuccore/',
        'example': 'NC_005946.1',
    },
    {
        'name': "NCBI GI number",
        'key': 'gi',
        'http': 'https://www.ncbi.nlm.nih.gov/genbank/sequenceids/',
        'example': '81941549',
    },
    {
        'name': 'GenBank GenPept',
        'key': 'genpet_acc',
        'comment': 'protein',
        'http': 'https://www.ncbi.nlm.nih.gov/protein',
        'example': 'AAT09660.1',
    },
    {
        'name': 'EMBL-EBI',
        'key': 'embl_protein_id',
        'comment': 'EMBLs European Bioinformatics Institute (EMBL-EBI)',
        'http': 'https://www.ebi.ac.uk/ena/browser/api/embl/',
        'example': 'AAT09660.1',
    },
    # UniProt
    {
        'name': 'SwissPalm',
        'key': 'uniprotkb_acc',
        'comment': 'protein',
        'http': 'https://www.swisspalm.org/',
        'example': 'Q6GZX4',
    },
    {
        'name': "UniProtKB accession",
        'key': 'uniprotkb_acc',
        'comment': 'protein',
        'http': 'https://www.uniprot.org/uniprotkb',
        'example': 'Q6GZX4',
    },
    {
        'name': "UniParc ID",
        'key': 'uniparc',
        'comment': 'protein',
        'http': 'https://www.uniprot.org/uniparc'
        'example': 'UPI00003B0FD4',
    },
    {
        'name': "UniProtKB ID",
        'key': 'uniprotkb_id',
        'comment': 'protein',
        'http': 'https://www.uniprot.org/uniprotkb',
        'example': '001R_FRG3G',
    },
    {
        'name': "UniRef100",
        'key': 'uniref100',
        'comment': 'protein family classification',
        'http': 'https://www.uniprot.org/help/uniref',
        'example': 'UniRef100_Q6GZX4',
    },
    {
        'name': "UniRef90",
        'key': 'uniref90',
        'comment': 'protein family classification',
        'http': 'https://www.uniprot.org/help/uniref',
        'example': 'UniRef90_Q6GZX4',
    },
    {
        'name': "UniRef50",
        'key': 'uniref50',
        'comment': 'protein family classification',
        'http': 'https://www.uniprot.org/help/uniref',
        'example': 'UniRef50_Q6GZX4',
    },
    {
        'name': 'UniProt Proteomes',
        'key': 'proteome_id',
        'comment': 'proteome',
        'http': 'https://www.uniprot.org/proteomes/',
        'example': 'UP000008770',
    },

    #protein family
    {
        'name': 'InterPro',
        'key': 'interpro_id',
        'comment': 'protein family',
        'http': 'http://www.ebi.ac.uk/interpro/',
        'example': 'IPR007031',
    },
    {
        'name': "PconsFam Accession",
        'key': 'pfam_acc',
        'comment': 'Pfam domain',
        'http': 'https://pconsfam.bioinfo.se',
        'example': 'PF04947',
    },
    {
        'name': "PconsFam ID",
        'key': 'pfam_id',
        'comment': 'Pfam domain',
        'http': 'https://pconsfam.bioinfo.se',
        'example': 'Pox_VLTF3',
    },
    {
        'name': "PIRSF Number",
        'key': 'pirsf',
        'comment': 'protein family of protein information resource',
        'http': 'https://proteininformationresource.org/',
        'example': 'PIRSF000705',
    },
    {
        'name': "PIR-PSD accession",
        'key': '',
        'comment': 'PIR-International Protein Sequence Database (PIR-PSD)',
        'http': 'https://proteininformationresource.org/pirwww/dbinfo/pir_psd.shtml',
        'example': '',
    },


    # others
    {
        'name': "EMBL-GenBank-DDBJ accession",
        'key': 'embl_acc',
        'comment': 'Protein Expression and Purification Core Facility',
        'http': 'https://www.ebi.ac.uk/ena/browser/home',
        'example': 'AY548484',
    },
    {
        'name': "EMBL-GenBank-DDBJ accession",
        'key': 'genbank_acc',
        'comment': 'DNA',
        'http': 'https://www.ncbi.nlm.nih.gov/nuccore',
        'example': 'AY548484',
    },
    {
        'name': "EMBL-GenBank-DDBJ accession",
        'key': 'ddbj_acc',
        'comment': 'DNA',
        'http': 'https://getentry.ddbj.nig.ac.jp',
        'example': 'AY548484',
    },
    {
        'name': 'KEGG GENES',
        'key': 'kegg_gene',
        'comment': 'protein',
        'http': 'https://www.genome.jp/',
        'example': 'vg:2947773',
    },
    {
        'name': "PDB",
        'key': 'pdb_id',
        'comment': 'RCSB Protein Data Bank (RCSB PDB) ',
        'http': 'https://www.rcsb.org/',
        'example': 'pdb102L',
    },
    {
        'name': 'MIM'
        'key': 'mim_id'
        'comment': 'Online Mendelian Inheritance in Man (OMIM)',
        'http': 'https://www.omim.org/'
        'example': '617688',
    },
    {
        'name': 'Gene Ontology',
        'key': 'go',
        'comment': 'ontology',
        'http': 'http://geneontology.org/',
        'example': 'GO:0006355',
    },
    {
        'name': "Ensembl ID",
        'key': 'ensembl_id',
        'comment': 'genome assembly: ENS(species)(object type)(identifier).(version)',
        # The third part is a one- or two-letter object type. 
        # For example E for exon, FM for protein family, G for gene, 
        # GT for gene tree, P for protein, R for regulatory feature and T for transcript.
        'http': 'https://useast.ensembl.org/index.html',
        'example': 'ENSMUSG00000017167.6',
    },


    # archived
    {
        'name': "UniGene",
        'key': '',
        'comment': 'protein',
        'http': 'https://www.ncbi.nlm.nih.gov/UniGene',
        'example': '',
    },    


   

    #customary definition
    {
        'name': "protein sequence",
        'key': "protein sequence",
        'comment': 'protein',
        'http': '',
        'example': '',
    },
    {
        'name': "EC number",
        'key': 'ec',
        'comment': 'protein',
        'http': '',
        'example': '',
    },

]
