def vtkGen(numSamples,pipeName,dreamDir,workDir=None):
	'''
	Generate <numSamples> microstructures
	for every stats file contained in workDir\_stats folder

	Input:
	* numSamples - number of microstructures to generate
					using a single stats file
	* dreamDir - folder containing DREAM3D.exe
	* pipeName - pipeline to run
	* workDir  - folder containing the pipeline and _stats folder

	Output:
	* vtk files containing phase IDs
	  for each generated microstructure

	Marat I. Latypov, 2016
	Georgia Tech Lorraine
	marat.latypov@georgiatech-metz.fr
	'''

	import os
	import shutil
	import timeit
	from subprocess import call

	if workDir == None:
		workDir = os.getcwd()

	os.chdir(dreamDir)

	# define directories
	statDir = workDir + '\\_stats'
	if not os.path.exists(statDir):
		print 'ERROR! _stats folder is not found.'
		return

	vtkDir  = workDir + '\\vtk'
	if not os.path.exists(vtkDir):
		os.makedirs(vtkDir)

	# define names of common files
	genStatFile = workDir + '\\stats.dream3d'
	genVtkFile = workDir + '\\msOut.vtk'

	# define the pipeline to run
	pipe = workDir + '\\' + pipeName
	runPipe = 'PipelineRunner -p %s' % pipe

	startTime = timeit.default_timer()

	errMsg = '\nERROR! vtk file msOut was not found.\n' + \
		'Check\n- Dream.3D pipeline (path, vtk output file name)\n' + \
		'- Stats files in _stats folder\n'

	for root, dirs, filenames in os.walk(statDir):
		for f in filenames:
			for ii in range(numSamples):

				iFileName = os.path.splitext(f)[0]
				statFile = os.path.join(root, f)
				shutil.copyfile(statFile,genStatFile)

				call(runPipe, shell=True)
				if not os.path.isfile(genVtkFile):
					print errMsg
					return
				vtkFile = vtkDir + '\\%s_%02d.vtk' % (iFileName, ii+1)
				shutil.copyfile(genVtkFile,vtkFile)
				print 'Done with %s' % iFileName

	finTime = timeit.default_timer() - startTime
	print '\n%.2f min spent on generation of %d vtk files' % ((finTime/60.0), len(filenames))

	if len(filenames) == 0:
		print 'ERROR! No stats file found'

	return