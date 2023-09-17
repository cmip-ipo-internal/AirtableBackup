# AirtableBackup
A library for backing up airtable data. 

<div>
<img src='https://wcrp-cmip.org/wp-content/uploads/2023/08/CMIP_Logo_RGB_Negative.png' style='width:200px;float:right;position:absolute'/>
<img src='https://wcrp-cmip.org/wp-content/uploads/2023/08/CMIP_Logo_RGB_Positive.png' style='width:200px;float:left;position:relative'/>
<img src='https://wcrp-cmip.org/wp-content/uploads/2023/08/CMIP_Logo_RGB_Negative.png' style='width:200px;'/>
<img src='https://wcrp-cmip.org/wp-content/uploads/2023/08/CMIP_Logo_RGB_Positive.png' style='width:200px;float:left;position:relative'/>
</div>

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





## Contributors

[![Contributors](https://contrib.rocks/image?repo=cmip-ipo-internal/AirtableBackup)](https://github.com/cmip-ipo-internal/AirtableBackup/graphs/contributors)
