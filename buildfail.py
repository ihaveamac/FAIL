#!/usr/bin/env python2
import argparse, sys, glob, os, binascii
version = 1

if len(sys.argv) < 3:
    print 'include some files yo'
    print '  buildfail.py file.txt *.bin'
    sys.exit()

# totally stolen from ncchinfo_gen
inpFiles = []
existFiles = []
toWrite = []
# filename, size

for i in xrange(len(sys.argv)-2):
    inpFiles = inpFiles + glob.glob(sys.argv[i+2].replace('[','[[]')) #Needed for wildcard support on Windows

for i in xrange(len(inpFiles)):
    if os.path.isfile(inpFiles[i]):
        existFiles.append(inpFiles[i])

if existFiles == []:
    print 'these files don\'t exist'
    sys.exit()

print 'listing files that exist'
for filename in existFiles:
    fsize = format(os.stat(filename).st_size, 'x').rjust(8, '0')
    toWrite.append([filename, fsize])

archive = open(sys.argv[1], 'wb')
# http://stackoverflow.com/questions/16414559/trying-to-use-hex-without-0x
numberOfFiles = binascii.unhexlify('{:04x}'.format(len(toWrite)))
version = binascii.unhexlify('{:04x}'.format(version))
print 'creating header'
archive.write("FAIL" + version + numberOfFiles)
# header stuff
for i in toWrite:
    archive.write("FILE" + i[0].ljust(0x100, chr(0x00)) + binascii.unhexlify(i[1]))
# actual file data
print 'writing actual file data'
for i in toWrite:
    print 'writing: ' + i[0]
    filehandle = open(i[0])
    while True:
        filedata = filehandle.read(0x1000000)
        if filedata == '':
            break
        archive.write(filedata)
    filehandle.close()
archive.close()

print 'looks like it worked'
print 'wrote '+str(len(toWrite))+' files'
sys.exit()
