CypherSweep
CypherSweep is a multithreaded web vulnerability scanner tool designed to find exposed directories, admin interfaces, and bypass 403 forbidden responses. It utilizes Tor for IP rotation to avoid rate limiting and detection.
Features

Vulnerability Scanner: Searches for exposed directories and vulnerable endpoints
403 Bypass: Attempts various techniques to bypass 403 Forbidden responses
HTTP Response Analysis: Scans for sensitive information in HTTP responses
Tor Integration: Routes traffic through Tor for anonymity and IP rotation
Multithreaded: Optimized for performance with configurable thread count
Rate Limiting: Configurable request rate limiting to avoid detection

Installation
Prerequisites

Python 3.6+
Tor (bundled in the package)

Setup

Clone the repository:
git clone https://github.com/michaelajilore/CypherSweep
cd cyphersweep

Install required Python packages:
pip install -r requirements.txt

Verify Tor folder structure:

Ensure you have a Torfolder directory containing:

tor subdirectory with tor.exe
torrc.txt configuration file





Directory Structure
CypherSweep/
├── cyphersweep.py
├── requirements.txt
├── README.md
└── Torfolder/
    ├── tor/
    │   └── tor.exe
    └── torrc.txt
Usage
Run the tool:
python cyphersweep.py
Main Menu Options

Vulnerability Search: Scans a domain for common vulnerabilities
403 Bypass: Attempts to bypass 403 Forbidden responses
Scan HTTP Response: Analyzes HTTP responses for sensitive information
Help Menu: Displays help information
Settings: Configure thread count and rate limiting

Important Notes

Ensure nothing is running on ports 9050 and 9051 (used by Tor)
Use Ctrl+C to exit any scan and return to the main menu
This tool is designed for security research and penetration testing on authorized systems only

Configuration
Thread Settings

Default: Uses your system's CPU count
Can be manually configured in the Settings menu

Rate Limiting

Default: 50-70 requests before IP rotation
Can be adjusted in the Settings menu

Disclaimer
This tool is intended for legal security testing with proper authorization. Users are responsible for compliance with applicable laws and regulations. Unauthorized scanning of systems is illegal and unethical.
License
MIT License
Author
By Michael Ajilore
