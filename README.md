# RYVCP Registration Automation Bot 

A robust, fault-tolerant Python and Selenium automation tool built to assist the Nyagatare Youth Volunteers in efficiently bulk-registering members into the Rwanda Youth Volunteers Management System (RYVCP).

## The Problem
Registering hundreds of volunteers into a modern, multi-step web portal is highly time-consuming and prone to human error. Furthermore, manual data entry was constantly disrupted by slow network connections, server timeouts, and hidden UI modals, turning a simple administrative task into a days-long hurdle for the youth volunteers team.

## The Solution
I built this automated engine to take over the heavy lifting. The bot reads volunteer data directly from an Excel spreadsheet and acts as a high-speed, invisible user. It navigates the RYVCP portal, handles identity verification, inputs contact and education details, selects location dropdowns, and confirms registration without requiring any human intervention.

## Key Features & Highlights
* **"Tank Mode" Network Handling:** Built with a custom "Gatekeeper" script that constantly monitors internet connectivity. If the hotspot/network drops, the bot gracefully pauses and instantly resumes the moment the connection returns.
* **Smart Name Verification:** Uses an adaptive algorithm to test different name combinations (prioritizing longer Kinyarwanda names) against the national ID verification endpoint to ensure a match.
* **Dynamic UI Bypassing:** Utilizes pure JavaScript execution to interact with modern web elements (like heavily styled React modals and custom dropdowns), bypassing visual glitches and scrollbar issues.
* **Auto-Healing & Retries:** If the government server lags or a page fails to load, the bot performs a hard refresh and retries the specific entry before officially marking it as a failure.
* **Live Excel Reporting:** Updates the original Excel dataset in real-time, tagging each volunteer as "Success", "Duplicate", or "Failed" with specific error reasons for easy follow-up.

## Tech Stack
* **Python**
* **Selenium WebDriver** (with `webdriver-manager` for automatic engine updates)
* **Pandas** (for seamless Excel data manipulation)

---
*Built to streamline administrative workflows and support the Nyagatare Youth Volunteers in their community initiatives.*
*Author: Hubert Nshuti Ngendahayo*
