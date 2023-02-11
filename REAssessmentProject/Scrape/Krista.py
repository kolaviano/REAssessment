import csv
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

license_type = "Pharmacist"
last_name = "L"

driver = webdriver.Chrome()

# Navigate to the Idaho License Verification website
driver.get("https://idbop.mylicense.com/verification/Search.aspx")

# Select the license type for pharmacists
license_type_select = Select(driver.find_element(By.ID, "t_web_lookup__license_type_name"))
license_type_select.select_by_visible_text(license_type)

# Enter the last name starting letter
last_name_input = driver.find_element(By.ID, "t_web_lookup__last_name")
last_name_input.send_keys(last_name)

# Submit the search form
search_button = driver.find_element(By.ID, "sch_button")
search_button.click()

xpath_link = ".//a"  # Xpath for pages
data = []  # Array of arrays

# Xpath for required information
elements = ['//*[@id="_ctl27__ctl1_first_name"]', '//*[@id="_ctl27__ctl1_m_name"]', '//*[@id="_ctl27__ctl1_last_name"]',
            '//*[@id="_ctl36__ctl1_license_no"]', '//*[@id="_ctl36__ctl1_license_type"]', '//*[@id="_ctl36__ctl1_status"]',
            '//*[@id="_ctl36__ctl1_issue_date"]', '//*[@id="_ctl36__ctl1_expiry"]', '//*[@id="_ctl36__ctl1_last_ren"]']
x = 0
r = 0

# Locate table and rows
rows = driver.find_elements(By.XPATH, "//table[@id='datagrid_results']/tbody/tr")

num_rows = len(rows)  # Get number of rows
row = rows[num_rows-1]  # Get to the rows for pages
cell = row.find_element(By.XPATH, ".//td")
counter = len(cell.text)//2  # Get number of pages

while r <= counter:  # Loop for number of pages
    r = r + 1
    rows = driver.find_elements(By.XPATH, "//table[@id='datagrid_results']/tbody/tr")
    num_rows = len(rows)
    row = rows[num_rows-1]
    i = 1
    z = 0
    y = 0
    while i <= num_rows-2:  # Loop for number of rows each page
        row = rows[i]
        cell = row.find_element(By.XPATH, ".//td")
        link = cell.find_element(By.XPATH, ".//a")

        # Click the name of the person to get required info
        link.click()

        # Focus on the new tab
        windows = driver.window_handles
        driver.switch_to.window(windows[1])

        for z in range(1):  # Number of sub array = 1
            sub_array = []
            num_elements = 9
            z = z + 1

            for y in range(num_elements):  # Number of needed information = 9
                req = driver.find_element(By.XPATH, elements[y])
                sub_array.append(req.text)  # Input to sub array
                y = y + 1
            data.append(sub_array)  # Append to array of arrays

        # Close the Tab
        close_button = driver.find_element(By.ID, "btn_close")
        close_button.click()

        # Focus on the primary tab
        windows = driver.window_handles
        driver.switch_to.window(windows[0])
        i = i + 1

    rows = driver.find_elements(By.XPATH, "//table[@id='datagrid_results']/tbody/tr")
    num_rows = len(rows)
    row = rows[num_rows-1]
    cell = row.find_element(By.XPATH, ".//td")
    if r >= counter:  # If >= number of pages
        link = cell.find_element(By.XPATH, xpath_link + "[" + str(counter) + "]")
        if x == 0:
            link.click()
        x = x + 1
    else:
        link = cell.find_element(By.XPATH, xpath_link + "[" + str(r) + "]")
        link.click()

with open("Pharmacists_L.csv", "w", newline="") as file:
    writer = csv.writer(file)
    # Write header
    writer.writerow(["First Name", "Middle Name", "Last Name", "License Number", "License Type", "Status",
                     "Original Issued Date", "Expiry", "Renewed"])
    # Write array of arrays
    writer.writerows(data)

# Close the driver
driver.quit()
