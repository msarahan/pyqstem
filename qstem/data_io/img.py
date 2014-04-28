"""
QSTEM - image simulation for TEM/STEM/CBED
    Copyright (C) 2000-2010  Christoph Koch
    Copyright (C) 2010-2013  Christoph Koch, Michael Sarahan

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

"""
Reads/writes to .img files (the original QSTEM data format)

File format from:
http://elim.physik.uni-ulm.de/?page_id=873
"""

import numpy as np
import struct

header_format = "iiiiiiiiddd"
header_size = 56
header_version = 1


class ioIMG(object):
    def read(self, filename, verbose=False):
        """
        Reading binary data of legacy QSTEM img format

        Parameters
        ----------
        filename : string
            The input filename to read from
        verbose : bool
            If True, outputs information as data is read.

        Returns
        -------
        img : ndarray
            The read image data
        comment : string
            The image's comment string
        thicknessOrDefocus : float
            The thickness that the image was recorded at.  Also abused to
            hold defocus instead of thickness.
        dx : float
            The resolution of the image in the horizontal direction
        dy : float
            The resolution of the image in the vertical direction
        parameters : list of floats
            an arbitrary list of parameters.  The order is known only in the
            context of the file, and no provision for annotating the file with
            labels for parameters exists.
        """

        # open the file and define the file ID (fid):
        # for some reason, this doesn't work:
        #with open(filename,'rb') as f:
        # use this instead:
        f = open(filename, "rb")
        # there are 8 4-byte ints followed by 3 8-byte doubles
        header = struct.unpack(header_format, f.read(header_size))

        headerSize = header[0]
        assert (headerSize == header_size)

        # read additional parameters from file, if any exist:
        paramSize = header[1]

        commentSize = header[2]

        Nx = header[3]
        Ny = header[4]

        complexFlag = header[5]
        dataSize = header[6]
        doubleFlag = (dataSize==8*(complexFlag+1))
        complexFlag = bool(complexFlag)

        version = header[7]
        assert(version == header_version)

        thicknessOrDefocus=header[8]

        dx = header[9]
        dy = header[10]

        if paramSize > 0:
            parameters = list(np.fromfile(file=f, dtype=np.float64, count=paramSize));
            if verbose:
                print('{:d} Parameters:'.format(paramSize))
                print(parameters)
        else:
            parameters = []

        # read comments from file, if any exist:
        if commentSize > 0:
            comment = struct.unpack("{:d}s".format(commentSize), f.read(commentSize))[0]
        else:
            comment = ""

        if verbose:
            print('io_IMG read {:s}: {:d} x {:d} pixels'.format(filename, Nx, Ny))

        if complexFlag:
            if doubleFlag:
                if verbose:
                    print('64-bit complex data, {:.3f}MB\n'.format(Nx*Ny*16/1048576))
                img = np.fromfile(file=f, dtype=np.complex128, count=Nx*Ny)
            else:
                if verbose:
                    print('32-bit complex data, {:.3f}MB'.format(Nx*Ny*8/1048576))
                img = np.fromfile(file=f, dtype=np.complex64, count = Nx*Ny)
        else:
            if doubleFlag:
                if verbose:
                    print('64-bit real data, {:.3f}MB\n'.format(Nx*Ny*8/1048576))
                img = np.fromfile(file=f, dtype=np.float64, count=Nx*Ny)
            else:
                if verbose:
                    print('32-bit real data, {:.3f}MB\n'.format(Nx*Ny*4/1048576))
                img = np.fromfile(file=f, dtype=np.float32, count=Nx*Ny)
        img=img.reshape(Ny,Nx)
        
        return img, comment, thicknessOrDefocus, dx, dy, parameters

    def write(self, array, output_file, comment="", thicknessOrDefocus=0.0, dx=1.0, dy=1.0, parameters=[]):
        """Write an IMG file given the array data
    
        Parameters
        ----------
        array : ndarray
            The data array to write to file
        output_file : string
            The file to output to.  Should have .img as its extension (not added for you)
        comment : string
            the file's comment
        thicknessOrDefocus : float
            The thickness or defocus at which this array represents
        dx : float
            The lateral resolution of this image, in nm/pixel
        dy : float
            The vertical resolution of this image, in nm/pixel
        parameters : list of floats
            An arbitrary list of parameters.  The order is known only by external programs,
            and there is no provision in the file format to assign names or meaning to parameters.

        Returns
        -------
        (None - writes output to file given as output_file)
        """
            
        complex_flag = np.issubdtype(array.dtype, np.complex)
        nx = array.shape[1]
        ny = array.shape[0]
        f = open(output_file, "wb")
        f.write(struct.pack(header_format, header_size, len(parameters), len(comment),
                            nx, ny, int(complex_flag), array.dtype.itemsize, header_version,
                            thicknessOrDefocus, dx, dy))
        f.write(struct.pack("{:d}d".format(len(parameters)), *parameters))
        f.write(comment)
        array.tofile(f)
