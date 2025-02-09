#!/bin/bash
#conda init bash
#conda activate documentbrowser; 
conda activate /opt/anaconda3/envs/documentbrowser
python -m airtable_backup --write --attachments
