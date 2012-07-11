#!/usr/bin/env python

import os
import argparse
import string
import re

class RegExps( object ):
    def __init__( self ):
        pass

    removeTrailingSpaces = re.compile( '[\t ]*$' ) 



def findFiles( startDir, fileExt ):

    contents    = os.listdir( startDir )

    files   = [ x for x in contents if os.path.isfile( os.path.join( startDir, x ) ) and x.endswith( fileExt ) ]
    dirs    = [ x for x in contents if os.path.isdir( os.path.join( startDir, x ) ) ]

    for f in files:
        filePath = os.path.join( startDir, f )
        oldFilePath = filePath + '.old'
        print filePath

        os.rename( filePath, oldFilePath )

        dst = open( filePath, 'wb' )

        for line in open( oldFilePath, 'rb' ).readlines():
            # remove the CR and make it LF
            temp = string.replace( line, '\r\n', '\n' )
            temp = string.replace( temp, '\r', '\n' )

            # remove tabulators and replace them with spaces
            temp = string.replace( temp, '\t', '    ' )

            # remove trailing spaces
            temp = RegExps.removeTrailingSpaces.sub( '', temp )

            dst.write( temp )

        dst.close()

    for d in dirs:
        findFiles( os.path.join( startDir, d ), fileExt )


if __name__ == '__main__':

    parser = argparse.ArgumentParser( description='Micazook source code file normalizer.' )
    parser.add_argument( '-p', dest='startDir', type=str, default='./',
                        help='starting directory path default local' )
    parser.add_argument( '-e', dest='extension', type=str, default='',
                        help='file extension' )
    parser.add_argument( '-r', dest='recursive', type=int, default=1,
                       help='recursive mode, default true')

    args        = parser.parse_args()

    startDir    = args.startDir
    recursive   = args.recursive
    fileExt     = args.extension
    
    findFiles( startDir, fileExt )
