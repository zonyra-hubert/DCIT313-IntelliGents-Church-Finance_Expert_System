# DCIT313-Group_Alpha-Church_Finance_Expert_System

## Group Members

1. Desmond Sedem Kojo Dedzoe - 22101911 - Role: Programmer
2. Zonyra Hubert - 22167843 - Role: Programmer
3. Derrick Pemboni 22019381- Role: Programmer
4. Henry Edem Amekor- 22109636 - Role: Knowledge Engineer
5. Henry Ampomah Nana Kwesi -22047836 - Role: Programmer 
6. Natasha Cobblah -22013436 - Role: Project Manager
7. Cheryl Abena Asantewaa Kwakye -22081315 - Role: Knowledge Engineer 


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
2. Install the required python library: `pip install pyswip`
3. Run the interface: `python interface/app.py`
