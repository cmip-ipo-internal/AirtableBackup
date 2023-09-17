'''
A script to backup the entire workspace in Airtable. 
This was designed for use by the IPO. 

Author and Maintainer - contact: 
Daniel Ellis (@wolfiex)
CMIP IPO Technical Officer. 
daniel.ellis (at) ext.esa.int

All copies of this program shall retain the original header statements as provided above. 
Additional features may be pushed on github, and the authors name and changes appended below. 
'''


from .__init__ import AirtableBackup
import tqdm
import argparse

def main():
    parser = argparse.ArgumentParser(description='Airtable Backup Script')
    parser.add_argument('--write', action='store_true', help='Enable writing to disk')
    parser.add_argument('--attachments', action='store_true', help='Enable downloading attachments')
    args = parser.parse_args()

    backup = AirtableBackup()
    backup.WRITE = args.write
    backup.ATTACHMENTS = args.attachments

    backup.start()

if __name__ == "__main__":
    main()

