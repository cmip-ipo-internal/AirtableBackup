# AirtableBackup
A library for backing up airtable data. 

<div>
<img src='https://wcrp-cmip.org/wp-content/uploads/2023/08/CMIP_Logo_RGB_Negative.png' style='width:200px;float:right;position:absolute'/>
<img src='https://wcrp-cmip.org/wp-content/uploads/2023/08/CMIP_Logo_RGB_Positive.png' style='width:200px;float:left;position:relative'/>
<img src='https://wcrp-cmip.org/wp-content/uploads/2023/08/CMIP_Logo_RGB_Negative.png' style='width:200px;'/>
<img src='https://wcrp-cmip.org/wp-content/uploads/2023/08/CMIP_Logo_RGB_Positive.png' style='width:200px;float:left;position:relative'/>
</div>
<a href="https://zenodo.org/badge/latestdoi/692810980"><img src="https://zenodo.org/badge/692810980.svg" alt="DOI"></a>


## Setup
For the code to function, we must fist set up our credentials as environmental variables in the 
`.bash_profile` or `.bashrc` 

e.g. 
```bash
export AIRTABLE_API_KEY="<enter your api key here>"
export AIRTABLE_BACKUP='/Users/name/directory'

```

## Usage

```bash
python -m airtable_backup --write --attachments
```

## What is backed up?
- Bases (each base in a separate directory)
- Tables (these are saved as referenced csv files)
- Attachments (these are in directories named as the tables)
- Schema (the relationships and constraints of the fields in a table
- Names and id of any views generated from a table

## Important files, and file structure



## case example and timing 





```
*******************************************************************************************************************
 CMIP - International Project Office Backup
*******************************************************************************************************************

-------------------------------------------------------------------------------------------------------------------
 Backup Location         : /<insert path here>/AirtableBackups/backup_230917
 Save Tables|Attachments : True True
 Total Elapsed Time (min): 1.7039594173431396
 Total Backup Size       : 70.71 MB
-------------------------------------------------------------------------------------------------------------------
```



## Contributors

[![Contributors](https://contrib.rocks/image?repo=cmip-ipo-internal/AirtableBackup)](https://github.com/cmip-ipo-internal/AirtableBackup/graphs/contributors)
