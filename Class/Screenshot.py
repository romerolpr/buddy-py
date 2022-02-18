import re

from selenium import webdriver
from selenium.webdriver.common.alert import Alert

from webdriver_manager.chrome import ChromeDriverManager

from PIL import Image
from io import BytesIO
from pathlib import Path
from time import sleep

class Screenshot():

	def __init__(self):
		super(Screenshot, self).__init__()

		options = webdriver.ChromeOptions()
		options.add_argument("--headless")
		options.add_argument("--no-sandbox")
		options.add_argument("--log-level=3")

		self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
		self.props = {}

	def setProps(self, props = None):
		dic = {
	   		'topo': self.driver.find_elements_by_css_selector('header'),
	   		'banner': self.driver.find_elements_by_css_selector('.slick-banner, .nivoSlider'),
	   		'footer': self.driver.find_elements_by_css_selector('footer'),
	   		'mpi_home': self.driver.find_elements_by_css_selector('.thumbnails, .card-group'),
	   		'mpi_page': self.driver.find_elements_by_css_selector('section'),
	   		'mpi_page_aside': self.driver.find_elements_by_css_selector('aside'),
	   		'mpi_page_region': self.driver.find_elements_by_css_selector('#servicosTabsDois, .organictabs--regioes'),
	   		'mpi_page_breadcrumb': self.driver.find_elements_by_css_selector('#breadcrumb'),
	   	}
		value = (self.merge(self.props, dic))
		self.props = value if props is None else props

	def getProps(self):
		return self.props

	def kill(self):
		self.driver.quit()

	def create_path(self, path):
		Path(f'./Data/screenshot/{path}').mkdir(parents=True, exist_ok=True)

	def merge(self, d, e):
	    n = {**d, **e}
	    return n

	def add_props(self, prop, selector, method = False):

		try:
			dic = {
				prop: self.driver.find_elements_by_css_selector(selector) if not method else method
			}
			value = (self.merge(self.props, dic))

			self.setProps(value)

		except Exception as arg:
			print('Cannot add new prop', arg)

	def curl_url(self, url):
		try:
			self.url = self.driver.get(url)
			self.domain = self.get_domain(url)
			try:
				if Alert(self.driver).accept():
					print('Alert were identified... ok')
				else:
					print('Alert were identified... but not closed')
			except:
				print('Good... alert not found')
		except Exception as arg:
			print('Cannot curl url', arg)

	def get_domain(self, url):
		try:
			if 'localhost' not in url:
				newUrl = re.search(r'https?:\/\/(www\.)?(.*)\/', url).group(2)
			else:
				newUrl = re.search(r'localhost\/(.*)', url).group(1)
			return re.sub(r'\/+', '', newUrl)
		except Exception as arg:
			print('Cannot get domain name', arg)

	def take_screenshot(self, content_page, index = 0):

		try:

			if not self.getProps():
				self.setProps()

			for prop, elem in self.getProps().items():

				if content_page == prop:

					print('Getting screenshot...', content_page)
					self.driver.set_window_size(1366, self.driver.execute_script('return document.body.scrollHeight'))

					self.create_path(content_page)

					if len(elem) > 0:
						elem = elem[index]
						location = elem.location
						size = elem.size

						sleep(1)
						png = self.driver.get_screenshot_as_png()
						title = self.driver.title

						print('Saving screenshot...')
						self.save_screenshot(png, size, location, prop)

					else:
						print(f'Cannot find {content_page} from site')
						return False

					break
		
		except Exception as arg:
			self.kill()
			print('Cannot take screenshot', arg)

	def save_screenshot(self, image, size, location, prop):
		try:
			
			img = Image.open(BytesIO(image))

			img_props = {
				'left': location['x'],
				'top': location['y'],
				'right': location['x'] + size['width'],
				'bottom': location['y'] + size['height']
		   	}

			img = img.crop((img_props['left'], img_props['top'], img_props['right'], img_props['bottom']))
			img.save(f'Data/screenshot/{prop}/{prop}_{self.domain}.png')

		except Exception as arg:
			print('Cannot save screenshot', arg)