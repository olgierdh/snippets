#!/usr/bin/env python

import os
import argparse
import string
import re
import mmap
import uuid

class RegExps( object ):
    removeTrailingSpaces = re.compile( '[\t ]*$' )

class ReplaceData( object ):
    replacements = ( ( '\r\n', '\n', 'EOF1' ), ( '\r', '\n', 'EOF2' ), ( '\t', '    ', 'TAB' ) )

def mapfileLineGenerator( mappedFile ):
    line = mappedFile.readline()

    while line:
        yield line
        line = mappedFile.readline()

def findFiles( startDir, fileExt, recLevel, currLevel = 0 ):
    contents    = os.listdir( startDir )

    files   = [ x for x in contents if os.path.isfile( os.path.join( startDir, x ) ) and x.endswith( fileExt ) ]
    dirs    = [ x for x in contents if os.path.isdir( os.path.join( startDir, x ) ) and x[ 0 ] != '.' ]

    for f in files:
        originalFilePath    = os.path.join( startDir, f )
        oldFilePath         = os.path.join( startDir, "." + f ) + '.old'
        switchFiles         = False

        with open( originalFilePath, 'rb' ) as origFile:
            origFileMap = mmap.mmap( origFile.fileno(), 0, access = mmap.ACCESS_READ )

            #test if we have to convert the file
            exReplacements = [ x for x in ReplaceData.replacements if x[ 0 ] in origFileMap ]

            if len( exReplacements ) > 0:
                # write the detected problems
                for rep in exReplacements:
                    print "DETECTED: %s in %s" % ( rep[ 2 ], originalFilePath )

                with open( oldFilePath, 'wb' ) as oldFile:
                    for line in mapfileLineGenerator( origFileMap ):
                        # copy the line for further simplifications
                        temp = line

                        # remove the CR and make it LF
                        for t in ReplaceData.replacements:
                            temp = string.replace( temp, t[ 0 ], t[ 1 ] )

                        # remove trailing spaces
                        #temp = RegExps.removeTrailingSpaces.sub( '', temp )

                        oldFile.write( temp )

                # here we know that we need to switch the file with names
                switchFiles = True

            #let's close the map
            origFileMap.close()

        # switch files f1->tmp, f2->f1, tmp->f2
        if switchFiles:
            tmpFileName = os.path.join( startDir, str( uuid.uuid1() ) )
            os.rename( originalFilePath, tmpFileName )
            os.rename( oldFilePath, originalFilePath )
            os.rename( tmpFileName, oldFilePath )


    if recLevel == 0 or ( recLevel > 0 and currLevel < recLevel ):
        for d in dirs:
            findFiles( os.path.join( startDir, d ), fileExt, recLevel,
                    currLevel + 1 )


if __name__ == '__main__':

    parser = argparse.ArgumentParser( description='Micazook source code file normalizer.' )
    parser.add_argument( '-p', dest='startDir', type=str, default='./',
                        help='starting directory path default local' )
    parser.add_argument( '-e', dest='extension', type=str, default='',
                        help='file extension' )
    parser.add_argument( '-r', dest='recursive', type=int, default=1,
                       help='recursive mode, default 1, set 0 if you want to enable unlimited recursion')

    args        = parser.parse_args()

    startDir    = args.startDir
    recursive   = args.recursive
    fileExt     = args.extension

    findFiles( startDir, fileExt, recursive )

