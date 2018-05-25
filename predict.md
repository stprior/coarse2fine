* predict queries without evaluation

This sets out some steps followed to test generation of SQL queries from natural language 
against a previously unseen data model. Original repo is https://github.com/donglixp/coarse2fine

# The pretrained model data should be extracted to data_model.

# Include details of the table schema in data_model/wikisql/data/predict.tables.json 
based on similar files

# Include the questions in wikisql/data/predict.jsonl. This file includes fields for expected
answers but these can be left blank or set to other values based on records in the 
pred or test files.

# Install and start a Stanford Core NLP service locally

# run wikisql/annotate.py to transform files from data_model/wikisql/data to
annotated files in data_model/wikisql. This script has been modified to request POS tags
from Stanford CoreNLP, however the original paper says POS tags were added using spaCy.

# modify predict.sh as required for local environment, and run it.

# predict.py is called. This is based on evaluate.py but skips executing queries and evaluating
accuracy of results, and supports the output argument to write generated SQL to a file.

