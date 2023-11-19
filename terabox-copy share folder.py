import re, json, csv, time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from os.path import isfile, join, exists
from os import listdir, makedirs, rename, system
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyperclip

# options = Options()
# fp = webdriver.FirefoxProfile('C:\\Users\\Giang\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\wu1o7rje.crawl')
# options.binary_location = r'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
# options.set_preference("browser.download.dir", "E:\\")

root_path = "E:\\tờ rát SỜ\\Lemon"
# link = "https://www.terabox.app/sharing/link?surl=H3AMo75WnLBbbIt7PgquNg"
link = "https://www.terabox.app/sharing/link?surl=H3AMo75WnLBbbIt7PgquNg&path=%2FLemon"
waiting_time = 15


if __name__ == "__main__":
	driver = uc.Chrome(headless=False,use_subprocess=False)
	driver.get(link)
	time.sleep(5)
# driver = webdriver.Firefox(fp, executable_path=r'E:\\geckodriver.exe', options=options)




def check_login():
	try:
		temp = driver.find_element(By.CLASS_NAME, "username").text
		if "USER" in temp:
			return True
	except:
		return False
	return False

def scroll_last():
	number = 0
	list_box = driver.find_element(By.CLASS_NAME, "common-file-list-box")
	while len(list_box.find_elements(By.CLASS_NAME, "common-file-item"))>number:
		number = len(list_box.find_elements(By.CLASS_NAME, "common-file-item"))
		for t in range(40):
			driver.execute_script(f"document.getElementsByClassName('common-file-item')[{str(t)}].scrollIntoView()")
			# list_box.send_keys(Keys.PAGE_DOWN)
		time.sleep(1.5)
	return True

def get_files_structure():
	try:
		list_box = driver.find_element(By.CLASS_NAME, "common-file-list-box")
	except:
		time.sleep(5)
		list_box = driver.find_element(By.CLASS_NAME, "common-file-list-box")

	scroll_last()

	temp = list_box.find_elements(By.CLASS_NAME, "common-file-item")
	result = []

	path = str(driver.current_url)
	path = path.split(r"&path=%2F")
	if len(path)==1:
		path = []
	else:
		path = path[-1]
		path = path.split(r"%2F")

	for t in temp:
		res = {}

		res["dir"] = path

		te = t.find_elements(By.CLASS_NAME, "file-icon-dir")
		if len(te)>0:
			res["folder"] = True
		else:
			res["folder"] = False

		te = t.find_element(By.CLASS_NAME, "file-item-name-link")
		res["name"] = te.text

		te = t.find_element(By.CLASS_NAME, "file-item-size")
		res["size"] = te.text

		te = t.find_element(By.CLASS_NAME, "file-item-ctime")
		res["time"] = te.text

		result +=[res]

	return [q for q in result if not q["folder"]] , [p for p in result if p["folder"]], path


def copy_files(dir_path):
	links = link.split("&path=")[0]
	links = link + "&path=%2F" + "%2F".join(dir_path)
	driver.get(link)
	time.sleep(2)

	scroll_last()

	list_box = driver.find_element(By.CLASS_NAME, "common-file-list-box")

	temp = list_box.find_elements(By.CLASS_NAME, "common-file-item")

	for g in range(0,len(temp),19):
		for t in range(g,g+19):
			try:
				te = temp[t].find_elements(By.CLASS_NAME, "file-icon-dir")
				if len(te)!=0: continue
			except:
				continue

			driver.execute_script(f"document.getElementsByClassName('file-item-checkbox')[{str(t)}].scrollIntoView()")


			te = temp[t].find_element(By.CLASS_NAME, "file-item-checkbox")
			if "selected" not in te.get_attribute("class"):
				te.click()

		driver.find_element(By.CLASS_NAME, "file-select-save").click()
		time.sleep(1.5)


		folder_list_add = driver.find_element(By.CLASS_NAME, "common-folder-list")

		already_have_folder = False
		taba = folder_list_add.find_elements(By.CLASS_NAME,"folder-item")
		for ta in range(len(taba)):
			if "Lemon" in str(taba[ta].text):
				already_have_folder = True
				stt = ta
		if not already_have_folder:
			driver.find_element(By.CLASS_NAME,"create-dir").click()
			for i in range(len("New Folder ")):
				driver.find_element(By.CLASS_NAME,"folder-name-text").send_keys(Keys.BACK_SPACE)
			driver.find_element(By.CLASS_NAME,"folder-name-text").send_keys("Lemon")
			driver.find_element(By.CLASS_NAME,"folder-name-commit").click()
		else:
			driver.execute_script(f"document.getElementsByClassName('folder-item')[{str(stt)}].scrollIntoView()")
			folder_list_add = driver.find_element(By.CLASS_NAME, "common-folder-list")
			taba = folder_list_add.find_elements(By.CLASS_NAME,"folder-item")
			for ta in range(len(taba)):
				if "Lemon" in str(taba[ta].text):
					taba[ta].click()

		driver.find_element(By.CLASS_NAME, "create-confirm").click()

		time.sleep(5)

		while True:
			dialog = driver.find_element(By.CLASS_NAME, "dialog-box")
			if "File saved successfully" in dialog.text:
				break
			else:
				time.sleep(1)

		dialog.find_element(By.CLASS_NAME, "icon-close").click()
		time.sleep(1)

		# Reset checkbox
		driver.find_element(By.CLASS_NAME, "common-file-list-header").find_element(By.CLASS_NAME, "file-list-checkbox").click()
		time.sleep(0.5)
		driver.find_element(By.CLASS_NAME, "common-file-list-header").find_element(By.CLASS_NAME, "file-list-checkbox").click()



			

















if __name__ == "__main__":

	# print("waiting for login...")
	# while True:
	# 	if check_login():
	# 		break
	# 	else: 
	# 		time.sleep(5)
	# print("login")

	print("get files structure")

	files_list, folders, dir_path = get_files_structure()

	print(files_list)

	copy_files(dir_path)

	# system("pause")



















# already_click = []

def upload_file(f):
	global root_path

	def press_upload():
		try_times = 1
		while True:
			form = driver.find_element(By.ID, 'form-container-anchor').value_of_css_property("display")
			print(type(form))
			print(form)
			if form != "none":
				try:
					pyperclip.copy( f)
				except:
					pass
				print("try press upload "+str(try_times))
				driver.find_element(By.CLASS_NAME, "type_switcher").text
				time.sleep(2)
				temp = driver.find_element(By.ID, 'fileInput').get_attribute("value")
				if len(temp)>5:
					for g in range(20):
						driver.find_element(By.ID, 'fileInput').send_keys(Keys.BACK_SPACE)

					driver.find_element(By.ID, 'fileInput').send_keys(join(root_path, f))
				else:
					driver.find_element(By.ID, 'fileInput').send_keys(join(root_path, f))
			else:
				time.sleep(3)
				pass

			time.sleep(3)
			# Neu dien duoc key name thi return True
			try:
				driver.find_element(By.ID, 'name_inp').send_keys(" ")
				break
			except:
				pass
			try_times +=1
		# time.sleep(3)
		return True

	press_upload()
	print(f)
	pyperclip.copy( f)



	# Combo
	file_combo = " ".join(f.split('_')[:-1]) 
	title = driver.find_element(By.ID, 'name_inp')

	if len(str(title.get_attribute("value")))<5:
		try:
			title.send_keys( f"bondage shibari rope latex fetish "+file_combo )
		except:	
			print("recaptcha done ?")
			system("pause")
			title.send_keys( f"bondage shibari rope latex fetish "+file_combo )


		boxes = driver.find_element(By.CLASS_NAME, 'radio-boxes').find_elements(By.TAG_NAME, 'label')
		for b in boxes:
			if "Straight" in b.text:
				b.click()

		category = driver.find_elements(By.CLASS_NAME, 'cat_label')
		for c in category:
			if "Amateur" in c.text or "Bondage" in c.text or "Fetish" in c.text or "Asian" in c.text :
				c.click()

		# Bondage (BDSM), Shibari rope, latex bondage
		tags = driver.find_element(By.ID, 'tag_inp').find_element(By.TAG_NAME, 'input')
		tags.send_keys("Bondage (BDSM)")
		time.sleep(1)
		tags.send_keys(Keys.ENTER)

		tags = driver.find_element(By.ID, 'tag_inp').find_element(By.TAG_NAME, 'input')
		tags.send_keys("Shibari rope")
		time.sleep(1)
		tags.send_keys(Keys.ENTER)	

		tags = driver.find_element(By.ID, 'tag_inp').find_element(By.TAG_NAME, 'input')
		tags.send_keys("latex bondage")
		time.sleep(1)
		tags.send_keys(Keys.ENTER)



	# Check download
	print("loop wait successfully uploaded videos")

	while True:
		text_form = driver.find_element(By.CLASS_NAME, "form-container").text
		if "successfully uploaded" in text_form:
			driver.find_element(By.ID, "upload_form_button").click()
			break
		else:
			time.sleep(5)

	print("click uploaded")

	while True:
		try:
			time.sleep(3)
			if EC.alert_is_present():
				driver.switch_to.alert.accept()
				print("video too short... skip")
				time.sleep(2)
				driver.get(link)
				return True
		except:
			pass
		current_url = driver.current_url

		if "users/videos" in current_url:
			time.sleep(2)
			break

	driver.get(link)

	return True

def update_already_upload():
	global files
	fa = open("already_upload.txt","r",encoding="utf8")
	ta = fa.read().split("\n")
	fa.close()
	for t in ta:
		try:
			files.remove(t)
		except:
			pass
	return True

if __name__ == "__main__":
	files = [f for f in listdir(root_path) if isfile(join(root_path, f) ) ]
	# print(files)
	update_already_upload()

	while len(files)>0:

		dur, count = with_opencv(join(root_path, files[0]))
		if count/30 > 65:
			upload_file(files[0])
	
		fa = open("already_upload.txt","a",encoding="utf8")
		fa.write(files[0]+"\n")
		fa.close()

		files = files[1:]


	driver.close()


