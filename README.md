# RYVCP Volunteer Registration Automation Bot

A Python automation system built to **bulk-register citizens into the Rwanda Youth Volunteers (RYVCP) platform** in a fast, reliable, and fault-tolerant way.

The tool was created to help **Nyagatare Youth Volunteers** register large numbers of people efficiently during community mobilization campaigns.

Instead of manually filling hundreds of web forms, this bot performs the entire process automatically using Selenium.

---

# Why This Project Exists

During volunteer registration campaigns in **Nyagatare District**, volunteers had to manually register hundreds of citizens on the RYVCP portal.

This process was:

- extremely **slow**
- **error-prone**
- affected by **unstable internet connections**
- difficult because of **multi-step forms and dynamic UI components**

To solve this, I built an automation system that reads citizen data from Excel and registers them automatically on the platform.

This reduced registration time from **days of manual work to a fully automated process.**

---

# What the Bot Does

The program acts like an **automated user** on the RYVCP system.

It automatically:

1. Logs into the RYVCP portal
2. Reads citizen data from an Excel spreadsheet
3. Opens the volunteer registration form
4. Performs identity verification
5. Fills contact and education details
6. Selects sector, cell, and village
7. Submits the registration
8. Records results back into Excel

Each entry is labeled as:

- ✅ Success  
- 🟡 Duplicate  
- 🔴 Failed  

---

# Technical Highlights

### Smart Identity Verification
The bot intelligently tests multiple **name combinations** to match the national ID verification system when exact matches fail.

### Network Resilience ("Tank Mode")
The system constantly monitors internet connectivity.  
If the connection drops, the bot **pauses automatically and resumes when the network returns**.

### Dynamic UI Handling
Uses **JavaScript execution through Selenium** to interact with complex elements such as:

- custom dropdowns
- React-based modals
- dynamically loaded form elements

### Auto-Retry System
If a server error or timeout occurs, the bot **retries the operation automatically** instead of failing immediately.

### Live Excel Reporting
After each registration attempt, the system updates the Excel file with:

- processing status
- error messages
- duplicate detection

This makes follow-up work easy.

---

# Tech Stack

- **Python**
- **Selenium WebDriver**
- **Pandas**
- **webdriver-manager**
- **ChromeDriver**

---

# Data Workflow

```
Excel File (citizens_data.xlsx)
            ↓
      Python Bot
            ↓
 RYVCP Volunteer Portal
            ↓
 Updated Excel Results
```

---

# 📌 Project Purpose

This project demonstrates how automation can be used to **support real community initiatives** by eliminating repetitive administrative work.

It was built to help **Nyagatare Youth Volunteers focus on mobilizing people instead of spending hours on manual data entry.**

---

**Author**  
Hubert Nshuti Ngendahayo
