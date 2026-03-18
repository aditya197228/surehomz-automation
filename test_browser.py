from core.browser import create_driver, get_base_url, close_driver

driver = create_driver()
url = get_base_url()
driver.get(url)

input("Press ENTER to close browser...")
close_driver(driver)