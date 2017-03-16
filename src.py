# Open a file dialog and extract spectral information, aggregate to file
import essentia
from essentia.standard import *
from heightmap import getSpectrums
from pprint import pprint
import Tkinter as tk
import tkFileDialog
import json

## Open dialog for user to select files
root = tk.Tk()
root.withdraw()
fileNames = tkFileDialog.askopenfilenames()

loadedAudioFiles = []

for fileName in fileNames:
	loader = MonoLoader(filename = fileName)
	loadedAudioFiles.append(loader())


dataPools = []
dataPoolsAggregated = []
fftArrays = []
extractor = Extractor()


for audioFile in loadedAudioFiles:
	currentExtractor = extractor(audioFile)
	##getSpectrums(audioFile, 512, 2048)
	dataPools.append(currentExtractor)
	dataPoolsAggregated.append(PoolAggregator(defaultStats = ["mean", "min", "max",])(currentExtractor))



# Output JSON
for index, dataPool in enumerate(dataPools):
	YamlOutput(filename = fileNames[index].replace('.wav', '') + '_analysis.json', format = 'json')(dataPool)

# Output aggregated JSON
for index, aggregatedPool in enumerate(dataPoolsAggregated):
	YamlOutput(filename = fileNames[index].replace('.wav', '') + '_aggregated_analysis.json', format = 'json')(aggregatedPool)

# Output heightmaps
##for index, fftArrays in enumerate(fftArrays):
##	with open('data%d.txt' % index, 'w') as outfile:
##		json.dump(fftArrays[index], outfile)