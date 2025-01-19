# TailScale Auto Auth Token Generator

## Overview
The **Boot2Root CTF Auth Token Generator** is a Python tool designed to automate the generation of authentication tokens for participants and machines in a Boot2Root Capture The Flag (CTF) event. This tool is part of the ["Building a Free CTF Platform"](https://medium.com/@s0pln3rr0r/building-a-free-ctf-platform-bfcpt-3f2918e6e028) blog series, which guides you through creating your own free and customizable CTF platform.

## Features
- **Token Generation**: Automatically generates and manages authentication tokens for participants and machines.
- **Excel Integration**: Outputs participant and machine data, including tokens, into an easy-to-use Excel file.
- **Seamless Integration**: Designed to work with Boot2Root CTF platforms built using the blog series.
- **Customizable**: Easily adapt the tool for specific CTF requirements or participant management.

## Screenshots

### 1. Generated Excel File
The tool creates an Excel file with details of participants and machines, including their generated authentication tokens.

![Excel File Example](https://cdn-images-1.medium.com/max/1000/1*OFOblV2zIlJLPDIGKTo2QQ.png)  
(*Placeholder: Replace this with a screenshot of the generated Excel file.*)

---

### 2. Tool Interface
Here’s how the tool looks when running in your terminal or console:

![Tool Interface](https://cdn-images-1.medium.com/max/1000/1*iAdEx46hZfNmlJ8hM48xgQ.png)  
(*Placeholder: Replace this with a screenshot of your tool's terminal interface.*)

---

## Prerequisites
- Python 3.8 or later
- Python libraries: `Requests`, `Pandas`, `os` and `openpyxl`.
- A valid Tailscale API key
- Your Boot2Root CTF environment configured as per the blog series

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/s0pln3rr0r/TailScale-Auto-Auth-Token-Generator.git
   cd tailscale-auto-auth-token-generator
Install the required dependencies:
```bash
pip install -r requirements.txt
```
Usage
Update the script generate_machine_invites.py with your Tailscale API key and CTF organization details.

Run the script to generate tokens for all participants and machines:

```bash
python generate_machine_invites.py
```
The script will generate an Excel file (tokens.xlsx) containing the tokens.
