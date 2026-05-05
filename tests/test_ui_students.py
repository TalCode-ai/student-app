import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


# תיקון fixture + צמצום time.sleep
@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

# בדיקה לטעינת העמוד בדפדפן
def test_open_students_page(driver):
    driver.get("http://127.0.0.1:5000")

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "tbody tr"))
    )

    assert "127.0.0.1" in driver.current_url

# בדיקה שטבלת הסטודנטים עולה
def test_students_table_is_displayed(driver):
    driver.get("http://127.0.0.1:5000")

    table = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.TAG_NAME, "table"))
    )

    assert table.is_displayed()

#בדיקה שהדאטהבייס מכיל לפחות תלמיד אחד
def test_students_table_has_data(driver):
    driver.get("http://127.0.0.1:5000")

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "tbody tr"))
    )

    rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
    assert len(rows) >= 1  # לפחות שורה אחת של נתונים

#בדיקה להוספת סטודנט
def test_add_student_ui(driver):
    driver.get("http://127.0.0.1:5000")

    name_input = driver.find_element(By.ID, "nameBox")
    age_input = driver.find_element(By.ID, "ageBox")
    add_button = driver.find_element(By.ID, "btAdd")

    name_input.send_keys("QA Test")
    age_input.send_keys("25")
    add_button.click()

    # מחכים שהתלמיד יופיע בטבלה
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "tbody tr"))
    )

    rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
    assert any("QA Test" in row.text for row in rows)

#מחיקת סטודנט
def test_delete_qa_test(driver):
    driver.get("http://127.0.0.1:5000")

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "tbody tr"))
    )
    # יצירת סטודנט
    driver.find_element(By.ID, "nameBox").send_keys("QA Delete Test")
    driver.find_element(By.ID, "ageBox").send_keys("25")
    driver.find_element(By.ID, "btAdd").click()

    time.sleep(2)
    # מציאת סטודנט
    rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
    student_id = None
    for row in rows:
        if "QA Delete Test" in row.text:
            student_id = row.find_elements(By.TAG_NAME, "td")[0].text
            break

    assert student_id is not None
    # מחיקת סטודנט
    driver.find_element(By.ID, "idBox").send_keys(student_id)
    driver.find_element(By.ID, "btDelete").click()
    alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert.accept()

    time.sleep(2)
    # בדיקה שהסטודנט נמחק
    rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
    assert all(student_id not in row.text for row in rows)

#בדיקת עדכון גיל
def test_update_student_age(driver):
    driver.get("http://127.0.0.1:5000")

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "tbody tr"))
    )

    driver.find_element(By.ID, "nameBox").send_keys("Temp User")
    driver.find_element(By.ID, "ageBox").send_keys("20")
    driver.find_element(By.ID, "btAdd").click()

    time.sleep(2)

    rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
    student_id = None

    for row in rows:
        if "Temp User" in row.text:
            student_id = row.find_elements(By.TAG_NAME, "td")[0].text
            break

    assert student_id is not None

    id_box = driver.find_element(By.ID, "idBox")
    id_box.clear()
    id_box.send_keys(student_id)

    age_input = driver.find_element(By.ID, "ageBox")
    age_input.clear()
    age_input.send_keys("55")

    driver.find_element(By.ID, "btUpdate").click()

    alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert.accept()

    time.sleep(2)

    rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
    assert any("Temp User" in row.text and "55" in row.text for row in rows)

#הוספת סטודנט עם גיל לא חוקי
def test_add_invalid_age_qa_test(driver):
    driver.get("http://127.0.0.1:5000")

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "tbody tr"))
    )

    driver.find_element(By.ID, "nameBox").send_keys("Illegal age")
    driver.find_element(By.ID, "ageBox").send_keys("15")
    driver.find_element(By.ID, "btAdd").click()

    alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
    assert "age" in alert.text.lower()
    alert.accept()

# בדיקות שליליות- שם ריק, גיל לא תקין
def test_add_empty_name(driver):
    driver.get("http://127.0.0.1:5000")

    driver.find_element(By.ID, "ageBox").send_keys("25")
    driver.find_element(By.ID, "btAdd").click()

    alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
    assert "name" in alert.text.lower()
    alert.accept()

def test_add_text_age(driver):
    driver.get("http://127.0.0.1:5000")

    driver.find_element(By.ID, "nameBox").send_keys("Bad Age")
    driver.find_element(By.ID, "ageBox").send_keys("abc")
    driver.find_element(By.ID, "btAdd").click()

    alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
    assert "age" in alert.text.lower()
    alert.accept()


