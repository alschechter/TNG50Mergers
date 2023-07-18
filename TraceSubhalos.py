import illustris_python as il
import h5py
from astropy.cosmology import Planck15 as cosmo


def FollowSingleSubhalo(ID, snapshot, TreeFileNumber):
    basePath = '/n/holystore01/LABS/hernquist_lab/Lab/IllustrisTNG/Runs/L35n2160TNG/output/'
    treePath = '/n/holystore01/LABS/hernquist_lab/Lab/IllustrisTNG/Runs/L35n2160TNG/postprocessing/trees/SubLink/'
    treeFile = 'tree_extended.' + str(TreeFileNumber) + '.hdf5'
    
    f = h5py.File(treePath + treeFile, 'r')

    ratio = 1./10.
    fields = ['FirstProgenitorID', 'NextProgenitorID', 'DescendantID', 
              'SubhaloSFR', 'SubfindID', 'SubhaloID', 'MainLeafProgenitorID',
              'SubhaloMassType', 'SnapNum', 'TreeID']

    firstprogenitors = []
    nextprogenitors = []
    descendants = []
    faileddescendants = []
    difftree = []


    #gal = f['SubfindID']
    tree = il.sublink.loadTree(basePath,snapshot,ID,fields=fields, onlyMPB=False)
    print('Tree ID', tree['TreeID'])
    #numMergers = il.sublink.numMergers(tree,minMassRatio=ratio)
    bigfile = h5py.File(basePath + '/snapdir_0' + str(snapshot) + '/snap_0' + str(snapshot) + '.0.hdf5', 'r')
    z_header = bigfile['Header'].attrs['Redshift']
    t0 = cosmo.age(z_header) 
    
    if tree['TreeID'].any() != TreeFileNumber:
        print('THIS SUBHALO NOT IN TREE ' + str(TreeFileNumber) + ' ', tree['TreeID'])
        difftree.append(ID)
        return difftree
   
    else:
        print('this works')
        for fp in tree['FirstProgenitorID']:
                if f['SnapNum'][fp] == snapshot - 1:
                    #how to get redshifts of any snapshot in order to get lookback time for merger plots
                    bigfile = h5py.File(basePath + '/snapdir_0' + str(snapshot - 1) + '/snap_0' + str(snapshot - 1) + '.0.hdf5', 'r')
                    z_header = bigfile['Header'].attrs['Redshift']
                    age = cosmo.age(z_header) 
                    firstprogenitors.append([f['SubfindID'][fp], snapshot - 1, age])
                elif f['SnapNum'][fp] == snapshot - 2:
                    bigfile = h5py.File(basePath + '/snapdir_0' + str(snapshot - 2) + '/snap_0' + str(snapshot - 2) + '.0.hdf5', 'r')
                    z_header = bigfile['Header'].attrs['Redshift']
                    age = cosmo.age(z_header) 
                    firstprogenitors.append([[f['SubfindID'][fp]], [snapshot - 2], [age]])
                                 
        for np in tree['NextProgenitorID']:
            if f['SnapNum'][np] == snapshot - 1:
                bigfile = h5py.File(basePath + '/snapdir_0' + str(snapshot - 1) + '/snap_0' + str(snapshot - 1) + '.0.hdf5', 'r')
                z_header = bigfile['Header'].attrs['Redshift']
                age = cosmo.age(z_header) 
                nextprogenitors.append([f['SubfindID'][np], snapshot - 1, age])
            elif f['SnapNum'][np] == snapshot - 2:
                bigfile = h5py.File(basePath + '/snapdir_0' + str(snapshot - 2) + '/snap_0' + str(snapshot - 2) + '.0.hdf5', 'r')
                z_header = bigfile['Header'].attrs['Redshift']
                age = cosmo.age(z_header) 
                nextprogenitors.append([f['SubfindID'][np], snapshot - 2, age])
                
        for d in tree['DescendantID']:
            if f['SnapNum'][d] == snapshot + 1:
                bigfile = h5py.File(basePath + '/snapdir_0' + str(snapshot + 1) + '/snap_0' + str(snapshot + 1) + '.0.hdf5', 'r')
                z_header = bigfile['Header'].attrs['Redshift']
                age = cosmo.age(z_header) 
                descendants.append([f['SubfindID'][d], snapshot + 1, age])
            else: 
                faileddescendants.append(f['SnapNum'][d])
        
        returnlist = [firstprogenitors, nextprogenitors, descendants, faileddescendants, t0, difftree]
    

        return returnlist

        # print(np.shape(descendants))
        # print(descendants[0])
        # descID = descendants[0][0]
        # descsnap = descendants[0][1]
        # tree = il.sublink.loadTree(basePath,descID,descsnap,fields=fields, onlyMDB=True)
        # if tree['TreeID'].any() != 0:
        #     print('THIS SUBHALO NOT IN TREE 0', tree['TreeID'])
        
        # else:
        #     for d in tree['DescendantID']:
        #         if f['SnapNum'][d] == descsnap + 1:
        #             bigfile = h5py.File(basePath + '/snapdir_0' + str(descsnap + 1) + '/snap_0' + str(descsnap + 1) + '.0.hdf5', 'r')
        #             z_header = bigfile['Header'].attrs['Redshift']
        #             age = cosmo.age(z_header) 
        #             descendants.append([f['SubfindID'][d], descsnap + 1, age])
        #         elif f['SnapNum'][d] == descsnap + 2:
        #             bigfile = h5py.File(basePath + '/snapdir_0' + str(descsnap + 2) + '/snap_0' + str(descsnap + 2) + '.0.hdf5', 'r')
        #             z_header = bigfile['Header'].attrs['Redshift']
        #             age = cosmo.age(z_header) 
        #             descendants.append([f['SubfindID'][d], descsnap + 2, age])
                    
        #         else: 
        #             faileddescendants.append(f['SnapNum'][d])
  