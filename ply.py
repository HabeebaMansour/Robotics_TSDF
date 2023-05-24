import numpy as np
import os

class Ply(object):
    """Class to represent a ply in memory, read plys, and write plys.
    """

    def __init__(self, ply_path=None, triangles=None, points=None, normals=None, colors=None):
        """Initialize the in memory ply representation.

        Args:
            ply_path (str, optional): Path to .ply file to read (note only
                supports text mode, not binary mode). Defaults to None.
            triangles (numpy.array [k, 3], optional): each row is a list of point indices used to
                render triangles. Defaults to None.
            points (numpy.array [n, 3], optional): each row represents a 3D point. Defaults to None.
            normals (numpy.array [n, 3], optional): each row represents the normal vector for the
                corresponding 3D point. Defaults to None.
            colors (numpy.array [n, 3], optional): each row represents the color of the
                corresponding 3D point. Defaults to None.
        """
        # TODO:(DONE) If ply path is None, load in triangles, point, normals, colors.
        #       else load ply from file. If ply_path is specified AND other inputs
        #       are specified as well, ignore other inputs.
        # TODO:(DONE) If normals are not None make sure that there are equal number of points and normals.
        # TODO:(DONE) If colors are not None make sure that there are equal number of colors and normals.
        self.ply_path=ply_path
        self.triangles= triangles
        self.points=points
        self.normals=normals
        self.colors=colors
        
        #Path not provided
        if ply_path is None:
          #Points
          if points.shape[1] != 3 or len(points.shape) != 2:
            raise ValueError('Invalid points')
          self.points=points
          #Triangles
          if triangles is not None:
            if triangles.shape[1] != 3 or len(triangles.shape) != 2:
              raise ValueError('Invalid triangles')
            self.triangles=triangles
          #Normals
          if normals is not None:
            if normals.shape[1] != 3 or len(normals.shape) != 2:
              raise ValueError('Invalid normals')
            if normals.shape[0] != points.shape[0]:
              raise ValueError('Points and Normals are not equal')
            self.normals=normals
          #Colors
          if colors is not None:
            if colors.shape[1] != 3 or len(colors.shape) != 2:
              raise ValueError('Invalid colors')
            if colors.shape[0] != points.shape[0]:
              raise ValueError('Points and Colors are not equal')
            self.colors=colors

        #Path Provided
        #Invalid Path
        else:
          if os.path.isfile(ply_path)== False:
            raise NameError('Invalid path')

          self.ply_path=ply_path
          self.normals=normals
          self.points=points
          self.colors=colors
          self.triangles=triangles
          self.read(self.ply_path)
          

    def write(self, ply_path):
        """Write mesh, point cloud, or oriented point cloud to ply file.

        Args:
            ply_path (str): Output ply path.
        """
        # TODO:(DONE) Write header depending on existance of normals, colors, and triangles.
        # TODO:(DONE) Write points.
        # TODO:(DONE) Write normals if they exist.
        # TODO:(DONE) Write colors if they exist.
        # TODO:(DONE) Write face list if needed.
        
        if os.path.isfile(ply_path)== False:
          raise NameError('Invalid path')
          
        self.ply_path=ply_path

        header='ply\nformat ascii 1.0\nelement vertex ' + str(self.points.shape[0]) +'\nproperty float x\nproperty float y\nproperty float z\n'

        normals='property float nx\nproperty float ny\nproperty float nz\n'

        colors='property uchar red\nproperty uchar green\nproperty uchar blue\n'

        if self.normals is not None:
          header=header+normals

        if self.colors is not None:
          header=header+colors

        if self.triangles is not None:
          triangles='element face '+ str(self.triangles.shape[0]) +'\nproperty list uchar int vertex_index\nend_header\n'
          header=header+triangles
        else:
          header=header+'end_header\n'

        array=''

        #Points
        if self.normals is None and self.colors is None:
          for i in range(self.points.shape[0]):
            array= array+' '.join(map(str, self.points[i, :]))+'\n'

        #Points and normals
        if self.normals is not None and self.colors is None:
          for i in range(self.points.shape[0]):
            array= array+' '.join(map(str, self.points[i, :]))+ ' '+ ' '.join(map(str, self.normals[i, :]))+'\n'

        #Points and colors
        if self.normals is None and self.colors is not None:
          for i in range(self.points.shape[0]):
            array= array+' '.join(map(str, self.points[i, :]))+' '+ ' '.join(map(str, self.colors[i, :]))+'\n'

        #Points and normals and colors
        if self.normals is not None and self.colors is not None:
          for i in range(self.points.shape[0]):
            array= array+' '.join(map(str, self.points[i, :]))+' '+ ' '.join(map(str, self.normals[i, :]))+' '+' '.join(map(str, self.colors[i, :]))+'\n'
        
        header=header+array

        #triangles
        if self.triangles is not None:
          for i in range(self.triangles.shape[0]):
            trianglesarray='3 '
            trianglesarray=trianglesarray+' '.join(map(str, self.triangles[i, :]))+'\n'
            header=header+trianglesarray

        self.ply_path=ply_path
        with open(self.ply_path, 'w') as f:
          f.write(header)

    def read(self, ply_path):
        """Read a ply into memory.

        Args:
            ply_path (str): ply to read in.
        """
        # TODO:(DONE) Read in ply.
        
        if os.path.isfile(ply_path)== False:
          raise NameError('Invalid path')
        
        self.ply_path=ply_path
        myfile= []
        with open(self.ply_path) as f:
          for line in f:
            myfile.append(line.strip())

        #Number of points
        n=[int(s) for s in myfile[[myfile.index(i) for i in myfile if('element vertex' in i)][0]].split() if s.isdigit()][0]

        #End Header
        end_header_index=[myfile.index(i) for i in myfile if(i=='end_header')][0]+1

        #String with points,normals,colors
        spnc=myfile[end_header_index:end_header_index+n]

        #Triangles
        if len([myfile.index(i) for i in myfile if('element face' in i)])==1:
          
          #Number of triangles
          k=[int(s) for s in myfile[[myfile.index(i) for i in myfile if('element face' in i)][0]].split() if s.isdigit()][0]

          #String with triangles
          st=myfile[end_header_index+n:end_header_index+n+k]

          self.triangles = np.empty(shape=[0, 3], dtype=np.intc)
          for row in st:
            splitrow= row.split()
            if len(splitrow)!=4:
              raise ValueError('Triangle is not correct dimension')
            
            self.triangles = np.append(self.triangles,[[int(splitrow[1]), int(splitrow[2]), int(splitrow[3])]] , axis=0)

        #Points
        if len([myfile.index(i) for i in myfile if('property float' in i)])==3:
          self.points = np.empty(shape=[0, 3])
          for row in spnc:
            splitrow= row.split()
            
            if len(splitrow)!=3:
              raise ValueError('All 3 dimensions of point not provided')
            
            self.points = np.append(self.points,[[float(splitrow[0]), float(splitrow[1]), float(splitrow[2])]] , axis=0)
        
        #Points and normals and NO colors
        if len([myfile.index(i) for i in myfile if('property float' in i)])==6 and len([myfile.index(i) for i in myfile if('property uchar' in i)])==0:
          self.points = np.empty(shape=[0, 3])
          self.normals = np.empty(shape=[0, 3])
          for row in spnc:
            splitrow= row.split()
            
            if len(splitrow)!=6:
              raise ValueError('Points and Normals are not equal')
            
            self.points = np.append(self.points,[[float(splitrow[0]), float(splitrow[1]), float(splitrow[2])]] , axis=0)

            self.normals = np.append(self.normals,[[float(splitrow[3]), float(splitrow[4]), float(splitrow[5])]] , axis=0)


        #Points and colors and normals
        if len([myfile.index(i) for i in myfile if('property float' in i)])==6 and len([myfile.index(i) for i in myfile if('property uchar' in i)])==3:
          self.points = np.empty(shape=[0, 3])
          self.normals = np.empty(shape=[0, 3])
          self.colors = np.empty(shape=[0, 3], dtype=np.ubyte)
          
          for row in spnc:
            splitrow= row.split()

            if len(splitrow)!=9:
              raise ValueError('Points and Colors and Normals are not equal')
            
            self.points = np.append(self.points,[[float(splitrow[0]), float(splitrow[1]), float(splitrow[2])]] , axis=0)

            self.normals = np.append(self.normals,[[float(splitrow[3]), float(splitrow[4]), float(splitrow[5])]] , axis=0)

            self.colors= np.append(self.colors,[[int(splitrow[6]), int(splitrow[7]), int(splitrow[8])]] , axis=0)


        #Points and colors
        if (len([myfile.index(i) for i in myfile if('property float' in i)])+len([myfile.index(i) for i in myfile if('property uchar' in i)]))==6:
          self.points = np.empty(shape=[0, 3])
          self.colors = np.empty(shape=[0, 3], dtype=np.ubyte)
          for row in spnc:
            splitrow= row.split()

            if len(splitrow)!=6:
              raise ValueError('Points and Colors are not equal')

            self.points = np.append(self.points,[[float(splitrow[0]), float(splitrow[1]), float(splitrow[2])]] , axis=0)

            self.colors = np.append(self.colors,[[float(splitrow[3]), float(splitrow[4]), float(splitrow[5])]] , axis=0)
