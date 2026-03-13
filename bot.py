import time
import random 
import pandas as pd
import os
import sys
import socket
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    UnexpectedAlertPresentException, 
    NoAlertPresentException, 
    WebDriverException, 
    TimeoutException
)
from selenium.webdriver.common.keys import Keys 

# ==========================================
# 1. SETUP & CONFIGURATION
# ==========================================
os.system('cls' if os.name == 'nt' else 'clear')
print("======================================================")
print("   🤖 RYVCP VOLUNTEER BOT - TANK EDITION V6 (FINAL)")
print("======================================================")

INPUT_EMAIL = "kabagambegodfrey2020@gmail.com"
INPUT_PASSWORD = "!Volunteer123"
TARGET_SECTOR = "Nyagatare"
TARGET_CELL = "Nyagatare"
TARGET_VILLAGE = "Nyagatare I" 

EXCEL_FILE = 'citizens_data.xlsx'
OUTPUT_FILE = 'citizens_data_COMPLETED.xlsx'

LOGIN_URL = "https://ryvcp.police.gov.rw/"
VOLUNTEERS_URL = "https://ryvcp.police.gov.rw/dashboard/volunteers"

EDUCATION_OPTIONS = ["Primary", "O level", "A level"]

if not os.path.exists("debug_errors"):
    os.makedirs("debug_errors")

# ==========================================
# 2. HELPER FUNCTIONS
# ==========================================
def clean_phone(phone_val):
    if pd.isna(phone_val): return ""
    s = str(phone_val).strip()
    if s.endswith('.0'): s = s[:-2]
    s = ''.join(filter(str.isdigit, s))
    if len(s) == 9: s = '0' + s
    return s

def determine_education(edu_text):
    if pd.isna(edu_text) or str(edu_text).strip().lower() in ['nan', 'none', '']:
        return random.choice(EDUCATION_OPTIONS)
    
    val = str(edu_text).lower()
    if 'prim' in val: return "Primary"
    if 'o level' in val or 'tronc' in val or 'ordin' in val: return "O level"
    if 'a level' in val or 'second' in val or 'adv' in val: return "A level"
    if 'tvet' in val or 'prof' in val: return "Tvet"
    if 'diploma' in val: return "Advanced Diploma"
    if 'bachelor' in val or 'degree' in val or 'univ' in val: return "Bachelors Degree"
    if 'master' in val: return "Masters Degree"
    if 'phd' in val or 'doctor' in val: return "PHD"
    
    return random.choice(EDUCATION_OPTIONS)

def wait_for_internet():
    first_fail = True
    while True:
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=1.5)
            if not first_fail: print("\n   🌐 Internet restored!")
            return
        except OSError:
            if first_fail:
                print("   ⚠️ NETWORK LOST. Pausing program until internet returns...")
                first_fail = False
            time.sleep(5)

def force_click(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    time.sleep(0.3)
    driver.execute_script("arguments[0].click();", element)

def click_button_by_text(driver, wait, text):
    xpath = f"//button[contains(., '{text}')]"
    elem = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    force_click(driver, elem)

def select_dropdown(driver, wait, label_text, option_text, target_placeholder="Select"):
    for attempt in range(3):
        try:
            try:
                trigger_xpath = f"//*[contains(text(), '{target_placeholder}')]"
                trigger = driver.find_element(By.XPATH, trigger_xpath)
                force_click(driver, trigger)
            except:
                trigger_xpath = f"//label[contains(., '{label_text}')]/following-sibling::div"
                trigger = driver.find_element(By.XPATH, trigger_xpath)
                force_click(driver, trigger)
                
            time.sleep(1) 
            
            opt_xpath = f"//*[(@role='option' or ancestor::ul[@role='listbox']) and contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{option_text.lower()}')]"
            opt = wait.until(EC.presence_of_element_located((By.XPATH, opt_xpath)))
            force_click(driver, opt)
            time.sleep(0.5)
            return True
            
        except Exception:
            webdriver.ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
            time.sleep(1) 
            
    print(f"\n      [!] Failed to set '{label_text}'")
    return False

def take_snapshot(driver, person_name):
    try:
        safe_name = "".join([c for c in str(person_name) if c.isalpha()]).strip()
        driver.save_screenshot(f"debug_errors/{safe_name}_error.png")
    except: pass

# ==========================================
# 3. BROWSER & LOGIN
# ==========================================
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--log-level=3") 
    
    # EAGER LOADING: Tells Chrome not to wait for heavy images/trackers to finish loading. Massive speed boost.
    options.page_load_strategy = 'eager' 
    
    if os.path.exists("chromedriver.exe"):
        try:
            service = Service("chromedriver.exe")
            return webdriver.Chrome(service=service, options=options)
        except: pass

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def login(driver):
    print("🔐 Logging in...")
    wait_for_internet()
    driver.get(LOGIN_URL)
    wait = WebDriverWait(driver, 45)
    
    try:
        email_field = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Email Address')]/following::input[1] | //input[@type='email']")))
        email_field.clear()
        email_field.send_keys(INPUT_EMAIL)
        
        pass_field = driver.find_element(By.XPATH, "//*[contains(text(), 'Password')]/following::input[1] | //input[@type='password']")
        pass_field.clear()
        pass_field.send_keys(INPUT_PASSWORD)
        
        click_button_by_text(driver, wait, "Sign In")
        wait.until(EC.url_contains("dashboard"))
        print("✅ Logged in successfully!\n")
    except Exception as e:
        print("⚠️ Login failed. Retrying...")
        time.sleep(3)
        login(driver)

# ==========================================
# 4. CORE LOGIC (The Form Filler)
# ==========================================
def process_person(driver, row):
    wait = WebDriverWait(driver, 15) 
    
    id_num = str(row.get('id', row.get('id_number', ''))).replace('.0', '').strip()
    full_name = str(row.get('names', row.get('name', 'Unknown'))).strip()
    phone_clean = clean_phone(row.get('phone', row.get('phone_number', '')))
    email = str(row.get('email', '')).strip()
    
    # PRE-FLIGHT CHECK: Instant skip if ID is bad
    id_digits = ''.join(filter(str.isdigit, id_num))
    if len(id_digits) != 16:
        return "Failed", f"Invalid ID length ({len(id_digits)} digits)"

    # CHANGED: Auto-generate email based on name with random 2-digit number
    if email.lower() in ['nan', 'none', '', 'null']:
        # Extract only letters from the name and make it lowercase
        name_only_letters = "".join([c for c in full_name if c.isalpha()]).lower()
        if not name_only_letters:
            name_only_letters = "volunteer" # Fallback if name is totally blank/symbols
        
        # Generate a random 2-digit number (01 to 99)
        random_num = str(random.randint(1, 99)).zfill(2)
        
        email = f"{name_only_letters}{random_num}@gmail.com"
        
    edu_raw = row.get('education', row.get('Education', ''))
    chosen_edu = determine_education(edu_raw)

    try:
        driver.get(VOLUNTEERS_URL)
        driver.refresh()
        time.sleep(2)
        
        print("      > Form...", end="", flush=True)
        click_button_by_text(driver, wait, "Add New volunteer")

        # --- STEP 1: ID & SMART NAME ---
        print(" ID...", end="", flush=True)
        id_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'National ID Number')]/following::input[1] | //input[contains(@placeholder, 'XXXX')]")))
        id_field.clear()
        id_field.send_keys(id_num)
        
        name_field_xpath = "//*[contains(text(), 'Verify Identity')]/following::input[1] | //input[@placeholder='Enter first or last name']"
        wait.until(EC.visibility_of_element_located((By.XPATH, name_field_xpath)))
        
        name_parts = full_name.split()
        name_parts.sort(key=len, reverse=True) 
        combinations_to_try = name_parts + [full_name]
        
        verified = False
        print(" Names...", end="", flush=True)
        for attempt_name in combinations_to_try:
            if len(attempt_name) < 2: continue 
            
            name_field = driver.find_element(By.XPATH, name_field_xpath)
            name_field.clear()
            name_field.send_keys(attempt_name)
            click_button_by_text(driver, wait, "Verify Name")
            time.sleep(1.5) 
            
            try:
                click_button_by_text(driver, WebDriverWait(driver, 2), "Continue")
                time.sleep(1.5)
                if len(driver.find_elements(By.XPATH, "//*[contains(text(), 'Email Address')]")) > 0:
                    verified = True
                    print(f" ✅ ({attempt_name})\n      > Details...", end="", flush=True)
                    break
            except TimeoutException:
                pass 
                
        if not verified:
            take_snapshot(driver, full_name)
            return "Failed", "Name/ID mismatch"

        # --- STEP 2: CONTACT & EDUCATION ---
        email_field = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Email Address')]/following::input[1]")))
        email_field.clear()
        email_field.send_keys(email)
        
        phone_field = driver.find_element(By.XPATH, "//*[contains(text(), 'Phone Number')]/following::input[1]")
        phone_field.clear()
        phone_field.send_keys(phone_clean)
        
        if not select_dropdown(driver, wait, "Education Level", chosen_edu, "Select level"):
            take_snapshot(driver, full_name)
            return "Failed", "Education dropdown failed"
            
        click_button_by_text(driver, wait, "Next Step")

        try:
            wait.until(EC.presence_of_element_located((By.XPATH, "//label[contains(., 'Sector')]")))
        except TimeoutException:
            take_snapshot(driver, full_name)
            return "Failed", "Blocked from Step 3"

        # --- STEP 3: WORK LOCATION ---
        print(" Location...", end="", flush=True)
        
        if not select_dropdown(driver, wait, "Sector", TARGET_SECTOR, "Select"):
            return "Failed", "Sector dropdown failed"
        if not select_dropdown(driver, wait, "Cell", TARGET_CELL, "Select"):
            return "Failed", "Cell dropdown failed"
        if not select_dropdown(driver, wait, "Village", TARGET_VILLAGE, "Select"):
            return "Failed", "Village dropdown failed"
        
        click_button_by_text(driver, wait, "Next Step")

        # --- STEP 4: CONFIRMATION ---
        print(" Submitting...", end="", flush=True)
        click_button_by_text(driver, wait, "Confirm Registration")

        for _ in range(15):
            time.sleep(1)
            page_text = driver.page_source.lower()
            if "already exists" in page_text or "duplicate" in page_text or "already registered" in page_text:
                return "Duplicate", "Already in system"
            
            if "add new volunteer" in page_text and "confirm registration" not in page_text:
                return "Success", "Added successfully"
                
        take_snapshot(driver, full_name)
        return "Unknown", "Timeout saving"

    except Exception as e:
        take_snapshot(driver, full_name)
        return "Crash", f"Error: {str(e).splitlines()[0][:50]}"

# ==========================================
# 5. MASTER CONTROLLER
# ==========================================
def main():
    print("📖 Reading Excel file...")
    try:
        df = pd.read_excel(EXCEL_FILE, dtype=str)
        df.columns = [str(c).strip().lower() for c in df.columns] 
        
        if 'id' not in df.columns and 'id_number' not in df.columns:
            print("❌ ERROR: Excel file is missing the 'id' column.")
            sys.exit()
            
        df['process_status'] = ""
        df['process_message'] = ""
        print(f"✅ Loaded {len(df)} people.")
    except Exception:
        print("❌ ERROR: Cannot read 'citizens_data.xlsx'. Please ensure it exists and is closed.")
        sys.exit()

    driver = setup_driver()
    login(driver)
    
    print("======================================================")
    print("   🚀 RUNNING... DO NOT TOUCH THE MOUSE.")
    print("======================================================")

    for index, row in df.iterrows():
        wait_for_internet() 
        
        name = str(row.get('names', row.get('name', 'Unknown'))).upper()
        print(f"\n[{index+1}/{len(df)}] {name}")
        
        # SECOND CHANCE SYSTEM: Tries up to 2 times if there is a random crash/glitch
        for attempt in range(2):
            status, msg = process_person(driver, row)
            
            if status in ["Success", "Duplicate"]:
                break # It worked (or is duplicate), exit the retry loop
            
            if status == "Failed" and "Invalid ID length" in msg:
                break # Don't retry bad IDs, it's a waste of time
                
            if attempt == 0:
                print(f"      🔴 FAILED ({msg}). Retrying once to be sure...")
                time.sleep(2) # Brief pause before retry
        
        if status == "Success": 
            print(f" 🟢 SUCCESS: {msg}")
        elif status == "Duplicate": 
            print(f" 🟡 SKIPPED: {msg}")
        else: 
            print(f" 🔴 FAILED: {msg}")
        
        df.at[index, 'process_status'] = status
        df.at[index, 'process_message'] = msg
        
        try: df.to_excel(OUTPUT_FILE, index=False)
        except: pass

    print("\n🎉 ALL FINISHED! Check 'citizens_data_COMPLETED.xlsx'")
    driver.quit()

if __name__ == "__main__":
    main()