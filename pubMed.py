import sys
import os
import shutil
import re
import csv

def clean(f_in, f_out):
    """
    Clean pubMed references exported in Abstract format. Strips \n and concatenates related lines.
    The formatted references have a consistent structure:
    # [0] = '-----'
    # [1] = <journal details>
    # [2] = <paper title>
    # [3] = <authors>
    # [4] = <authors details>
    # [5] = <abstract>
    # [6] = <PMID>

    :param f_in: Name of text file containing pubMed references in Abstract format (e.g., 'refs.txt').
    :type f_in: string
    :param f_out: Name of new file that will be contain reformatted references (e.g., 'cleaned_refs.txt').
    :type f_out: string
    :return: None
    """
    
    # Read in all lines and remove line-break from lines with text.
    temp = []
    f_in = open(f_in, 'r')
    for line in f_in:
        if line == '\n':
            temp.append(line)
        else:
            temp.append(line.strip())
    f_in.close()

    # Cycle through all lines and concatenate text for each reference.
    temp2 = []
    temp2.append('-----')
    for i, line in enumerate(temp):
        if i > 0:
            if temp[i].split(' ')[0] == 'PMID:':
                temp2.append(temp[i].split(' ')[0] + ' ' + temp[i].split(' ')[1])
                temp2.append('-----')
            elif line == '\n' and temp[i-1] != '\n' and temp[i-1].split(' ')[0] != 'PMID:':
                temp2.append(new_line)
            elif line == '\n' and temp[i-1] == '\n':
                pass
            elif line != '\n' and temp[i-1] == '\n':
                new_line = line
            else:
                new_line = new_line + ' ' + line

    # Cycle through all lines and extract simpler form of journal reference
    temp3 = []
    temp3.append('-----')
    for i, line in enumerate(temp2):
        if i > 0:
            if temp2[i-1] == '-----':
                ref = line.split('.')
                line = ref[1][1:] + ref[2]
            temp3.append(line)

    # Some references have a Copyright line; lets remove it
    index_start = 0
    index_end = []
    temp4 = []
    for i, line in enumerate(temp3):
        if i > 0:
            if line == '-----':
                index_end = i
                ref = temp3[index_start+1 : index_start+6]
                ref.append(temp3[index_end - 1])
                index_start = index_end
                temp4.append('-----')
                for ref_line in ref:
                    temp4.append(ref_line)
    """ This leaves use with 6 lines per reference:
        [0] = journal info
        [1] = paper title
        [2] = authors
        [3] = author information
        [4] = abstract
        [5] = PMID """

    # Cycle through each line and write formatted references.
    f_out = open(f_out, 'w')
    f_out.write(temp4[0])
    f_out.write('\n')
    for i, line in enumerate(temp4):
        if i > 0:
            # Sometimes had back-to-back lines with PMIDs; skip these when writing file
            if temp4[i-1].split(' ')[0] == 'PMID:' and temp4[i].split(' ')[0] == 'PMID:':
                pass
            else:
                f_out.write(line)
                f_out.write('\n')
    f_out.close()

def select(f_sort, f_keep, f_reject, f_query):
    """
    :param f_sort: path to sort file (e.g., '../../../data/proc/sorting_refs.txt')
    :type f_sort: string
    :param f_keep: path to sort file (e.g., '../../../data/proc/refs_keep.txt')
    :type f_keep: string
    :param f_reject: path to sort file (e.g., '../../../data/proc/refs_reject.txt')
    :type f_reject: string
    :param f_query: path to sort file (e.g., '../../../data/proc/refs_query.txt')
    :type f_query: string
    :return: None
    """

    # Read in all lines and remove line-breaks.
    refs = []
    sort = open(f_sort, 'r')
    for line in sort:
        refs.append(line.strip())
    sort.close()
    os.remove(f_sort)

    # Open the keep, reject and query files ready to add references.
    keep = open(f_keep,'a')
    reject = open(f_reject,'a')
    query = open(f_query,'a')
    sort = open(f_sort,'w')
    refs_left = 1
    cur_ref = ['-----']
    ref_count = 0
    for i, line in enumerate(refs):
        if i > 0:
            if line == '-----':
                ref_count += 1
                print('\n')
                print(cur_ref[2],'\n\n',cur_ref[-2],'\n')
                ans = input('Processing references number {} for this session.\n\n'
                            'Do you want to (k)eep, (r)eject or (q)uery reference?\n'
                            'Or do you want to (s)top processing references?\n\n'.format(ref_count))
                if ans == 'k':
                    for ref_line in cur_ref:
                        keep.write(ref_line)
                        keep.write('\n')
                elif ans == 'r':
                    for ref_line in cur_ref:
                        reject.write(ref_line)
                        reject.write('\n')
                elif ans == 'q':
                    for ref_line in cur_ref:
                        query.write(ref_line)
                        query.write('\n')
                else:
                    for ref_line in cur_ref:
                        sort.write(ref_line)
                        sort.write('\n')
                    for j in range(i,len(refs)):
                        if refs[j] == '-----':
                            refs_left += 1
                        sort.write(refs[j])
                        sort.write('\n')
                    print('\n')
                    print('Thank you for your efforts. There are now', str(refs_left-ref_count), 'left to process.')
                    keep.close()
                    reject.close()
                    query.close()
                    sort.close()
                    # Save backups just in case something goes wrong along the way.
                    shutil.copy(f_keep, f_keep + '_bk')
                    shutil.copy(f_reject, f_reject + '_bk')
                    shutil.copy(f_query, f_query + '_bk')
                    shutil.copy(f_sort, f_sort + '_bk')
                    return
                cur_ref = ['-----']
            else:
                cur_ref.append(line)


def emailExtract(f_keep, pmid_emails_file, pmid_alone_file):
    """
     :param f_keep: path to sort file (e.g., '../../../data/proc/refs_keep.txt')
    :type f_keep: string
    """

# cd '/home/martin/Dropbox/Martin/Documents/research/projects/activeProjects/tDCSsurvey/src/code/pubMed'
# f_keep = 'refs_keep.txt'

    # Read in all lines and remove line-breaks.
    refs = []
    keep = open(f_keep, 'r')
    for line in keep:
        refs.append(line.strip())
    keep.close()

    # Create a list where each element contains the information for a single reference
    # Each element (e.g., refs_list[0]) will contain lists of the references, where
    # refs_list[n][4] will be the author info section and refs_list[n][6] will be
    # the PMID
    refs_list = [None] * 1600
    rl_index = 0
    cur_ref = ['','','','','','','']
    cr_index = 0
    for line in refs:
        cur_ref[cr_index] = line
    #    print('            Current reference index',cr_index)
        cr_index += 1
        if line.split(' ')[0] == 'PMID:':
            refs_list[rl_index] = cur_ref
            cur_ref = ['','','','','','','']
            cr_index = 0
    #        print('Currently processing reference', rl_index, 'PMID: ', line.split(' ')[1])
            rl_index += 1

    # Cycle through each reference and determine if there are emails in the authors
    # information section. If yes, store them along with the PMID. If not,
    # simply store the PMID
    pmid_emails = open(pmid_emails_file,'a')
    pmid_alone = open(pmid_alone_file,'a')
    for ref in refs_list:
        if not (ref == None):
            au_info = ref[4]
            emails = re.findall(r'[\w\.-]+@[\w\.-]+', au_info)
            for i, item in enumerate(ref):
                if item.split(' ')[0] == 'PMID:':
                    pmid = item.split(' ')[1]
            if len(emails) > 0:
                for i, email in enumerate(emails):
                    emails[i] = email.strip('.')
                emails.insert(0, pmid)
                # Add some blank values to have a total of 20 items
                for i in range(20-len(emails)):
                    emails.append(' ')
                data_to_save = ', '.join(emails)
                pmid_emails.write(data_to_save)
                pmid_emails.write('\n')
            else:
                pmid_alone.write(pmid)
                pmid_alone.write('\n')
    pmid_emails.close()
    pmid_alone.close()


def emailUnique(all_emails, emails_unique):
    """
    :param all_emails: .csv file containing all emails (including duplicates)
    :type all_emails: string
    :param all_emails: .csv file where unique emails will be stored
    :type all_emails: string
    """
    # Read in all references.
    emails = []
    with open(all_emails, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            emails.append(row)

    unique_emails = []
    for ref in emails:
        for item in ref:
            if item != '  ':
                if item != '-----':
                    unique_emails.append(item)

    unique_emails = list(set(unique_emails))

    with open(emails_unique, 'w') as f:
        for email in unique_emails:
            f.writelines(email.lstrip().strip() + ', ')

