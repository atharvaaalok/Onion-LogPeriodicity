from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

# Set the path to the webdriver executable (e.g., chromedriver)
webdriver_path = ""

# Create a new Chrome browser instance
driver = webdriver.Chrome(webdriver_path)
driver.maximize_window()

# Open the web page
driver.get("https://www.nhb.gov.in/OnlineClient/MonthlyPriceAndArrivalReport.aspx?enc=3ZOO8K5CzcdC/Yq6HcdIxJ4o5jmAcGG5QGUXX3BlAP4=")


# Make Lists for all data to download
# Place list
# Place_list = ["MUMBAI", "LASALGAON"]
Place_list = ["MUMBAI"]

# Year list 2000-2022 both inclusive
Year_list = list(range(2000, 2023))

# Month list
Month_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


# Download data for each of the above cases
for place in Place_list:
    for year in Year_list:
        for month in Month_list:
            
            month_count = Month_list.index(month) + 1
            print(f"{place}/{str(year)}_{str(month_count)}")

            # Find and select the center/state dropdown
            center_state_dropdown = Select(driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_LsboxCenterList"))
            center_state_dropdown.select_by_visible_text(place)

            time.sleep(2)

            # Find and select the year dropdown
            year_dropdown = Select(driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_ddlyear"))
            year_dropdown.select_by_visible_text(str(year))

            time.sleep(2)

            # Find and select the month dropdown
            month_dropdown = Select(driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_ddlmonth"))
            print(month)
            month_dropdown.select_by_visible_text(month)

            time.sleep(1)

            # Find and select the category dropdown
            category_dropdown = Select(driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_drpCategoryName"))
            category_dropdown.select_by_visible_text("VEGETABLES")

            time.sleep(1)

            # Find and select the crop dropdown
            crop_dropdown = Select(driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_drpCropName"))
            crop_dropdown.select_by_visible_text("ONION")

            time.sleep(1)

            # Find and select the variety dropdown
            variety_dropdown = Select(driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_ddlvariety"))
            variety_dropdown.select_by_visible_text("ONION")

            time.sleep(1)

            # Click the Search button
            search_button = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_btnSearch")
            search_button.click()

            # Wait for the table to load (you may need to adjust the time if the table takes longer to load)
            time.sleep(8)

            # Get the table data
            try:
                table = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_GridViewmonthlypriceandarrivalreport")
            except:
                print("NO TABLE FOUND")
                continue

            table_text = table.get_attribute('innerText')

            data_list = list(table_text)

            # Remove initial data till the actual numbers start
            newline_counter = 0
            element_counter = 0
            for element in data_list:
                element_counter = element_counter + 1
                if element == '\n':
                    newline_counter = newline_counter + 1
                if newline_counter == 11:
                    break
            
            data_list = data_list[element_counter:]

            print(data_list)

            file_name = f"{place.capitalize()}/{str(year)}_{month_count}.csv"
            with open(file_name, 'w', encoding='utf-8') as file:

                i = 0
                day_counter = 1
                # If two consecutive elements are '\n' then end the list there
                while day_counter < 32:
                    print("Day", day_counter)
                    tab_counter = 0
                    j = i
                    while data_list[j] == '\t':
                        tab_counter += 1
                        j += 1

                    file_row = []
                    
                    if tab_counter == 1:
                        i += 1
                        num_counter = 0
                        day_loop_counter = 0
                        while data_list[i] != '\t' and data_list[i] != '\n' and num_counter < 5:
                            day_loop_counter = 1
                            num_counter += 1
                            while data_list[i] != '\n':
                                file_row.append(data_list[i])
                                i += 1
                            file_row.append(',')
                            i += 1
                        while data_list[i] == '\n':
                            i += 1
                    else:
                        print("Tab Counter", tab_counter)
                        empty_rows = [',', ',', ',', ',', '\n'] * (tab_counter - 1)
                        file_row.extend(empty_rows)
                        day_counter += (tab_counter - 1)
                        i += tab_counter
                        num_counter = 0
                        day_loop_counter = 0
                        while data_list[i] != '\t' and data_list[i] != '\n' and num_counter < 5:
                            day_loop_counter = 1
                            num_counter += 1
                            while data_list[i] != '\n':
                                file_row.append(data_list[i])
                                i += 1
                            file_row.append(',')
                            i += 1
                        while data_list[i] == '\n':
                            i += 1

                    # Add row to file
                    if day_loop_counter == 0:
                        file_row.extend([',', ',', ',', ',', '\n'])
                    file_row[-1] = '\n'
                    print(file_row)
                    file_row_str = ''.join([str(elem) for elem in file_row])
                    file.write(file_row_str)
                    day_counter += 1



# Close the browser
driver.quit()