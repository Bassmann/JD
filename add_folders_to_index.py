import os
import argparse

def fast_scandir(dirname):
    subfolders = [f.path for f in os.scandir(dirname) if f.is_dir()]
    for dirname in list(subfolders):
        subfolders.extend(fast_scandir(dirname))
    return subfolders

# Initialize parser
parser = argparse.ArgumentParser(description="update the index with missing files for existing folders")

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
        year = dirdata[-3]
        categoryid = category.split('_')[0]
        categoryname = category.split('_')[1]
        jdid = basename.split()[0]
        if args.verbose:
            print(f'{areaname=}, {areaid=}, {categoryname}, {categoryid=}, {year}, {jdid=}')

        if not categoryid.startswith(areaid) or jdid.split('.')[0] != categoryid:
            print(f'Mismatch: area: {areaid} {areaname}, category: {categoryid} {categoryname}, id: {jdid}')
        else:
            outfile = f'{logseq}/jd24___{basename}.md'
            if not os.path.exists(outfile):
                print("Creating file " + outfile)
                with open(outfile, 'w') as out:
                    out.write("tags:: [[JD]]\n")
                    out.write("store:: file system\n")
                    out.write("year:: " + year + "\n")
                    out.write("area:: " + areaname + "\n")
                    out.write("category:: " + categoryname + "\n")
                    out.write("jdid:: " + basename + "\n")
