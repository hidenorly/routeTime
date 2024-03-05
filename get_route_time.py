#   Copyright 2024 hidenorly
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import argparse
import sys
import subprocess
import urllib.parse
from urllib.parse import urljoin
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WebUtil:
	@staticmethod
	def get_web_driver(width=1920, height=1080):
		options = webdriver.ChromeOptions()
		options.add_argument('--headless')
		tempDriver = webdriver.Chrome(options=options)
		userAgent = tempDriver.execute_script("return navigator.userAgent")
		userAgent = userAgent.replace("headless", "")
		userAgent = userAgent.replace("Headless", "")

		options = webdriver.ChromeOptions()
		options.add_argument('--headless')
		options.add_argument(f"user-agent={userAgent}")
		driver = webdriver.Chrome(options=options)
		driver.set_window_size(width, height)

		return driver

class RouteUtil:
	@staticmethod
	def generate_directions_link(lat1, lon1, lat2, lon2):
	    base_url = "https://www.google.com/maps/dir/?api=1"
	    origin = f"{lat1},{lon1}"
	    destination = f"{lat2},{lon2}"
	    params = {
	        "origin": origin,
	        "destination": destination
	    }
	    return base_url + "&" + urllib.parse.urlencode(params)

	@staticmethod
	def get_directions_duration(driver, url):
		driver.get(url)
		duration_element = None

		try:
			duration_element = WebDriverWait(driver, 10).until(
				EC.presence_of_element_located((By.XPATH, "//*[@id='section-directions-trip-0']/div[1]/div/div[1]/div[1]"))
			)
			if duration_element:
				duration = duration_element.text
				return duration
		except:
			pass

		return None


if __name__=="__main__":
	parser = argparse.ArgumentParser(description='Specify start_latitude start_logtitude dest_latitude dest_logtitude e.g. 35.681236 139.767125 35.6759323 139.7450316')
	parser.add_argument('args', nargs='*', help='')

	args = parser.parse_args()

	loc = args.args

	if len(loc)==4:
		directions_link = RouteUtil.generate_directions_link(loc[0], loc[1], loc[2], loc[3])
		print(directions_link)

		driver = WebUtil.get_web_driver()
		duration = RouteUtil.get_directions_duration(driver, directions_link)
		print("Estimated duration:", duration)
