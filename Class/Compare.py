import glob, cv2, os, numpy as np, pandas as pd
from .JSON import JSON as json

class Compare():

	def __init__(self):
		super(Compare, self).__init__()
		self.images = {}
		self.index = {}
		self.image_model = ''
		self.option = None
		self.JSONModel = None
		self.listsResult = {
			'results': [],
			'methodName': []
		}
		self.OPENCV_METHODS = None

	def setOpenCV_methods(self, methods):
		self.OPENCV_METHODS = methods
	def setJSONModel(self, jsonm):
		self.JSONModel = jsonm

	def setImagesModel(self, image):
		try:

			if os.path.isfile(os.getcwd() + image):
				img = cv2.imread(os.getcwd() + image)
				hist = cv2.calcHist([img], [0, 1], None, [8, 8], [0, 256, 0, 256])
				
				self.image_model = cv2.normalize(hist, hist).flatten()

		except Exception as arg:
			print('Cannot set histogram of image model', arg)

	def setOption(self, optionName):
		self.option = optionName
	def setImage(self, filename, image):
		self.images[filename] = image
	def setIndex(self, filename, image):
		self.index[filename] = image
	def addMethodName(self, methodName):
		self.listsResult['methodName'].append(methodName)
	def addResults(self, results):
		self.listsResult['results'].append(results)

	def getOption(self):
		return self.option
	def getImageModel(self):
		return self.image_model
	def getResults(self):
		return self.listsResult['results']
	def getMethodImage(self):
		return self.listsResult['methodName']
	def getIndex(self):
		return self.index
	def getImages(self):
		return self.images
	def getOpenCV_methods(self):
		return self.OPENCV_METHODS

	def getResultNumber(self):
		try:

			for item in self.getResults():
				print( [ x[0] for x in item ] )

		except Exception as arg:
			print('Cannot get number', arg)


	def load_container(self, path = '\\Index\\', ext = 'jpg'):
		try:
			for imagePath in glob.glob(os.getcwd() + path + r"\*." + ext):

				filename = imagePath[imagePath.rfind("/") + 1:]
				image = cv2.imread(imagePath)

				self.setImage(filename, cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

				hist = cv2.calcHist([image], [0, 1], None, [8, 8], [0, 256, 0, 256])

				self.setIndex(filename, cv2.normalize(hist, hist).flatten())

		except Exception as arg:
			print('Cannot load container', arg)

	def start_comparation(self, reverse = False):
		try:

			if len(self.index) == 0 or len(self.images) == 0 :
				print('You need to load container, please do "load_container" before.')
				return False

			if self.OPENCV_METHODS is None:
				print('You need to give OPENCV_METHODS, please do "setOpenCV_methods" before.')
				return False

			for (methodName, method) in self.OPENCV_METHODS:

				if methodName == self.option or self.option is None:

					results = {}
					reverse = False

					if methodName in ("Correlation", "Intersection"):
						reverse = True
					for (k, hist) in self.index.items():
						d = cv2.compareHist(self.getImageModel(), hist, method)

						if d >= float(0.76):
							results[k] = d

					self.addMethodName(methodName)
					results = sorted([(v, k) for (k, v) in results.items()], reverse = reverse)
					self.addResults(results)

		except Exception as arg:
			print('Cannot start comparations', arg)

	def save_xlsx(self, all = True):
		try:

			for i in range(len(self.getResults())):
				self.results['results'][i] = pd.DataFrame(self.results['results'][i])
				self.results['results'][i]['Metodo'] = self.listsResult['methodName'][i]
			
			df = pd.concat(self.getResults())
			writer = pd.ExcelWriter('results.xlsx', engine='xlsxwriter')
			df.to_excel(writer, sheet_name='Sheet1', index=False)
			writer.save()

		except Exception as arg:
			print('Cannot save in xlsx', arg)