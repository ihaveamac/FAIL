#!/usr/bin/env python2
import argparse, sys, os, binascii

if len(sys.argv) != 3:
    print 'pick a file to extract and a directory to put all the files in'
    print '  extractfail.py file.fail stuff'
    sys.exit()

if not os.path.isfile(sys.argv[1]):
    print sys.argv[1] + ' doesn\'t exist'
    sys.exit()

try:
    os.makedirs(sys.argv[2])
except OSError:
    if not os.path.isdir(sys.argv[2]):
        raise

archive = open(sys.argv[1], "rb")
archive.seek(0x0)
if archive.read(0x4) != "FAIL":
    print 'this isn\'t a "FAIL" archive'
    sys.exit()

archive.seek(0x4)
version = int(binascii.hexlify(archive.read(2)), 16)
print 'archive version: ' + str(version)
if version != 1:
    print 'archive version too new'
    print 'this script can handle up to version 1'
    sys.exit()

archive.seek(0x6)
numberOfFiles = int(binascii.hexlify(archive.read(2)), 16)
print 'number of files: ' + str(numberOfFiles)

toExtract = []
# filename, offset, size
currentOffset = 0x8 + (numberOfFiles * 0x108)
print currentOffset
for filenumber in range(0, numberOfFiles):
    archive.seek(0x8 + (filenumber * 0x108))
    fileheader_magic = archive.read(0x4)
    if fileheader_magic != "FILE":
        print 'incorrect magic found (should be "FILE")'
        archive.close()
        sys.exit()
    fileheader_name = archive.read(0x100).rstrip('\0')
    fileheader_size = int(binascii.hexlify(archive.read(0x4)), 16)
    toExtract.append([fileheader_name, currentOffset, fileheader_size])
    currentOffset += fileheader_size

# TODO: make this more memory efficient
for fileinfo in toExtract:
    print 'writing: ' + fileinfo[0]
    filehandle = open(sys.argv[2] + '/' + fileinfo[0], "wb")
    archive.seek(fileinfo[1])
    filedata = archive.read(fileinfo[2])
    filehandle.write(filedata)
    filehandle.close()

archive.close()

print 'looks like it worked'
print 'extracted '+str(len(toExtract))+' files'
sys.exit()
