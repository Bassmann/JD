import os
import argparse

def fast_scandir(dirname):
    subfolders = [f.path for f in os.scandir(dirname) if f.is_dir()]
    for dirname in list(subfolders):
        subfolders.extend(fast_scandir(dirname))
    return subfolders

# Initialize parser
parser = argparse.ArgumentParser(description="check the JD directory structure and point out issues such as wrong ids, missing index files and too deep directories")

# Adding optional argument
parser.add_argument("-d", "--Directory", help="The JD top directory", required=True)
parser.add_argument("-l", "--Logseq", help="The Logseq pages directory", required=True)
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
# Read arguments from command line
args = parser.parse_args()

dir = args.Directory
logseq = args.Logseq

folders = fast_scandir(dir)

folders.sort()
for folder in folders:
    dirname = os.path.dirname(folder)
    basename = os.path.basename(folder).replace('_', ' ')
    dirdata = dirname.split('/')

    if args.verbose:
        print(f'{folder=}, {dirname=}, {basename=}')
        print('')

    if basename.find(".") != -1:
        area = dirdata[-2]
        areaname = area.split('_')[1]
        areaid = area[0]
        category = dirdata[-1]
        categoryid = category.split('_')[0]
        categoryname = category.split('_')[1]
        jdid = basename.split()[0]
        if not categoryid.startswith(areaid) or jdid.split('.')[0] != categoryid:
            print(folder)
            print('-' * len(folder))
            print(f'Mismatch: {areaid=} {areaname=}, {categoryid=} {categoryname=}, {jdid=}')
            print('')

        if "Inbox" in basename:
            for root, dirs, files in os.walk(folder):
                if len(files) > 0:
                    print(root)
                    print('-' * (len(root)))
                    for filename in files:
                        print(filename)
                    print('')

        outfile = f'{logseq}/jd24___{basename}.md'
        if not os.path.exists(outfile):
            print(folder)
            print('-' * len(folder))
            print(f'Index file missing: {outfile}')
            print('')
    else:
        if len(dirdata) > 8:
            print(folder)
            print('-' * len(folder))
            print(f'Directory depth too deep')
            print('')

