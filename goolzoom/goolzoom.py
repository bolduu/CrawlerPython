from selenium import webdriver
from selenium.webdriver.common.keys import Keys

wd = webdriver.Chrome()
wd.get("http://es.goolzoom.com/")

#wd.implicitly_wait(5) # seconds
#pdt3 = wd.find_element_by_id("submitAlert")
#pdt3.click()


pdt4 = wd.find_element_by_id("TextDireccion")
pdt4.send_keys('albacete')
pdt4.send_keys(Keys.ENTER)

pdt2 = wd.find_element_by_id("panelLateralTopInmuebles")
pdt2.click()

#pdt = wd.find_element_by_id("BuscarDireccion")
#pdt.submit()

#inputElement.send_keys('1')

print "FINAL"

