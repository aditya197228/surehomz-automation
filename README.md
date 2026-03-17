# SureHomz Automation Framework

End-to-end automation testing framework for the SureHomz Channel Partner Portal.
Built with Selenium + Python.

## Status
🔒 Private — Work in progress

## Tech Stack
- Python + Selenium
- openpyxl (Excel)
- python-dotenv (credentials)
- webdriver-manager (ChromeDriver)

## Project Structure
```
surehomz-automation/
├── core/              → shared utilities
├── direct_booking/    → direct booking flows
├── login/             → login flow
├── results/           → test results
├── screenshots/       → failure screenshots
├── logs/              → run logs
├── .env               → credentials (never committed)
└── requirements.txt   → dependencies
```

## Environment Setup
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt