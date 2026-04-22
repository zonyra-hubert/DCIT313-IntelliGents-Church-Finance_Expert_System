# DCIT313-Group_IntelliGents-Church_Finance_Expert_System

## Group Members

1. dessy0905 - 22101911 - Role: Programmer
2. zonyra-hubert - 22167843 - Role: Programmer
3. Derry27 - 22019381- Role: Programmer
4. wtxn - 22109636 - Role: Knowledge Engineer 
5. henryampomah -22047836 - Role:  Programmer 
6. tasha -22013436 - Role: Project Manager
7. irealcheryl -22081315 - Role: Knowledge Engineer


## Project Description

This project implements a Knowledge-Based System (KBS) for Church Finance management. The system acts as an "Intelligent Agent" taking over manual entry review and financial routing.

Using SWI-Prolog as the inference engine and Python (with pyswip) as the user interface, it maps user inputs (perceptions) to logical actions (advice/conclusions). Features include:

- **Pattern Recognition**: Flags entries exceeding the expected 12-month average by 500%.
- **Constraint Satisfaction**: Prevents routing to closed or non-existent funds.
- **Member Status Logic**: Prompts for new profiles when guests attempt a General Tithe.
- **Expense Audit**: Validates expenses against predefined category budgets.
- **Financial Routing**: Automatically directs restricted vs. unrestricted funds to the proper ledger.
- **Reconciliation & Accountability**: Simplifies bank reconciliation and automatically generates detailed audit trails.

## Setup & Running

1. Ensure you have `swi-prolog` installed on your machine.
2. Install the required python libraries: 
   ```
   pip install -r requirements.txt
   ```
   or manually:
   ```
   pip install pyswip flask
   ```
3. Run the web interface: `python interface/app.py`
4. Open your browser and go to `http://localhost:5000`


## Features

The web interface provides the same functionality as the command-line version with an intuitive graphical interface:

- **Record Income**: Log tithes and donations with intelligent validation
- **Record Expense**: Track expenses with budget checking
- **Bank Reconciliation**: Verify deposits against system records
- **Tax Statements**: Generate IRS-compliant contribution statements
- **Audit Trail**: View complete transaction history

## Expert System Rules

The system implements several AI techniques:

- **Pattern Recognition**: Flags entries exceeding 500% of member's average giving
- **Constraint Satisfaction**: Prevents routing to closed/invalid funds
- **Member Status Logic**: Prompts for new profiles when guests give tithes
- **Expense Audit**: Validates expenses against predefined budgets
- **Financial Routing**: Automatically directs funds to correct ledgers

## Architecture

- **Frontend**: HTML/CSS/JavaScript with Bootstrap for responsive design
- **Backend**: Python Flask web framework
- **Knowledge Base**: SWI-Prolog for expert system rules
- **Database**: In-memory storage (can be extended to persistent storage)
