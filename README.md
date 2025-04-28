CypherSweep
                                                                          
 By Michael Ajilore


CypherSweep is a versatile web security reconnaissance tool designed to identify potential vulnerabilities in websites. It uses TOR for anonymity and employs various techniques including Google Dorking, 403 bypass attempts, and HTTP response analysis.
Features

Vulnerability Search: Scans domains using a comprehensive list of Google dorks to identify potentially vulnerable endpoints.
403 Bypass: Attempts to bypass 403 Forbidden responses using various techniques.
HTTP Response Analysis: Analyzes HTTP responses for common security issues.
TOR Integration: Routes all requests through TOR for anonymity and IP rotation.
Multi-threaded Operation: Optimizes scanning speed with configurable thread settings.

Customizable Settings:

Thread count
Rate limiting
Scan breadth



Installation

Clone the repository:

git clone https://github.com/michaelajilore/CypherSweep
cd cyphersweep

Install required packages:

pip install -r requirements.txt

Installation
Prerequisites

Python 3.6+
Tor (bundled in the package)

Verify Tor folder structure:

Ensure you have a Torfolder directory containing:

tor subdirectory with tor.exe
torrc.txt configuration file

Directory Structure
CypherSweep/
├── dork.py
├── requirements.txt
├── README.md
└── Torfolder/
    ├── tor/
    │   └── tor.exe
    └── torrc.txt
Usage
Run the tool:
python dork.py
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

Default: 20-30 requests before IP rotation
Can be adjusted in the Settings menu

Disclaimer
This tool is intended for legal security testing with proper authorization. Users are responsible for compliance with applicable laws and regulations. Unauthorized scanning of systems is illegal and unethical.
License
MIT License
Author
By Michael Ajilore
