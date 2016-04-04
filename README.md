# FAIL
This is basically a file archiving format nobody asked for, I guess.

I created this mostly because I wanted to practice with Python a bit. This is a file container that does nothing more than store the filename, its size, and the actual contents.

The name "FAIL" is from possibly all the things I've done so wrong making this, as well as all the things it doesn't support (like directories), and things I could have done better. But hey, I had fun.

## Usage
```bash
python buildfail.py myarchive.fail thing.bin *.zip game.3dsx
python extractfail.py myarchive.fail directory
```

## Format
The file is layed out like this:
* Base header (0x8 bytes)
* File headers, one for each file (0x108 bytes)
* Contents of all files joined together

The offset of a file is calculated by getting the size of all the headers combined plus the size of each file before it.

### Base header
Offset | Size | Description
--- | --- | ---
0x0 | 0x4 | Magic "FAIL"
0x4 | 0x2 | Archive format version
0x6 | 0x2 | Number of files

### File header
Offset | Size | Description
--- | --- | ---
0x0 | 0x4 | Magic "FILE"
0x4 | 0x100 | File name
0x4 | 0x4 | File size

## License
<a href="http://creativecommons.org/publicdomain/mark/1.0/"><img src="http://i.creativecommons.org/p/mark/1.0/88x31.png" alt="Public Domain Mark"></a>
