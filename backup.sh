#!/bin/bash
conda init bash
conda activate documentbrowser; python -m airtable_backup --write --attachments
