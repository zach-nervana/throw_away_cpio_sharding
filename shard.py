import glob
import os

# cpio files will be moved into `n` directories created inside /tmp
srcdir = '/mnt/local1/data/I1K/i1k_cpio_256'
destdir = '/tmp'
n = 2
remove_files_with_unusual_count = true
operation = 'cp'
# operation = 'ln'




filenames = glob.glob(srcdir + '/*.cpio')

# check that they are all the same size
def cpio_count(filename):
    raw = os.popen('cpio -it -F {filename} | wc -l'.format(filename=filename)).read().strip()
    return int(raw)

if remove_files_with_unusual_count:
    # the first cpio file should be full
    expected_count = cpio_count(sorted(filenames)[0])

    filenames = [filename for filename in filenames if cpio_count(filename) == expected_count]

# split filenames into n shards
shards = [[] for _ in range(n)]

for i, filename in enumerate(filenames):
    shards[i % n].append(filename)

# remove cpio files from each shard so as to make shards the correct
# size
target_length = min(map(len, shards))

for shard in shards:
    shard = shard[:target_length]

# figure out what the prefix is in the filename
prefix = '_'.join(os.path.basename(filenames[0]).split('_')[:-1])

# ensure destinate paths exist
for i in range(n):
    os.system('mkdir -p {dir}/{i}'.format(
        dir=destdir,
        i=i,
    ))

# copy files
for i, filenames in enumerate(shards):
    for j, filename in enumerate(filenames):
        os.system('{operation} {src} {dest}'.format(
            operation=operation,
            src=filename,
            dest='{dir}/{i}/{prefix}_{j}.cpio'.format(
                dir=destdir,
                i=i,
                prefix=prefix,
                j=j,
            )
        ))
