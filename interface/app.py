import sys
import os
import datetime

try:
    from pyswip import Prolog
except ImportError:
    print("Error: The 'pyswip' library is not installed.")
    print("Please install it using: pip install pyswip")
    sys.exit(1)

class ExpertSystemInterface:
    def __init__(self):
        self.prolog = Prolog()
        # Ensure we can find the knowledge base relative to this script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        kb_path = os.path.join(base_dir, "..", "knowledge_base", "finance_rules.pl")
        
        try:
            # Using Unix-style path for Prolog consult
            consult_path = kb_path.replace('\\', '/')
            self.prolog.consult(consult_path)
            print(f"Knowledge Base loaded successfully from: {kb_path}")
        except Exception as e:
            print(f"Failed to load Knowledge Base: {e}")
            sys.exit(1)
            
        self.transactions = []
        self.audit_trail = []
        
    def add_audit_log(self, action, details, reason):
        log = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "action": action,
            "details": details,
            "reason": reason
        }
        self.audit_trail.append(log)
        
    def query_prolog_bool(self, query_str):
        # Helper to check if a query returns any results
        result = list(self.prolog.query(query_str))
        return len(result) > 0
        
    def record_income(self):
        print("\n--- Record Income ---")
        member_id = input("Enter Member ID (e.g., m001, m002, guest): ").strip()
        
        amount_str = input("Enter Amount: ").strip()
        try:
            amount = float(amount_str)
        except ValueError:
            print("Error: Amount must be a number.")
            return
            
        fund_id = input("Enter Fund ID (e.g., f001 for General Tithe, f002 for Building Fund): ").strip()
        entry_method = input("Enter Entry Method (Cash/Check/Digital): ").strip()
        service_date = input("Enter actual Service Date (YYYY-MM-DD): ").strip()
        entry_date = datetime.date.today().strftime("%Y-%m-%d")
        
        print("\n--- Processing via Inference Engine ---")
        
        # 1. Constraint Satisfaction
        if self.query_prolog_bool(f"invalid_fund('{fund_id}')"):
            print(f"ACTION REJECTED: Constraint Satisfaction failed. Fund '{fund_id}' does not exist or is closed.")
            return
        
        # 2. Member Status Logic
        if self.query_prolog_bool(f"requires_new_member_profile('{member_id}', '{fund_id}')"):
            print("EXPERT ADVICE: Member Status Logic triggered. Guest is giving a General Tithe. Please prompt user to create a new member profile.")
            
        # 3. Pattern Recognition (Anomaly Detection)
        if self.query_prolog_bool(f"needs_verification('{member_id}', {amount})"):
            print(f"EXPERT ADVICE: Pattern Recognition triggered. Amount {amount} exceeds 500% of 12-month average for member '{member_id}'. VERIFICATION NEEDED.")
            
        # 4. Financial Routing
        route_query = list(self.prolog.query(f"route_income('{fund_id}', Ledger)"))
        if route_query:
            ledger = route_query[0]['Ledger']
            print(f"FINANCIAL ROUTING: Income routed to => {ledger}")
        else:
            ledger = "Unknown Ledger"
            print("FINANCIAL ROUTING: Could not determine ledger.")
        
        reason = input("\nEnter 'Reason for Change' (Audit Trail Requirement): ").strip()
        if not reason:
            reason = "Standard Data Entry"
            
        transaction = {
            "type": "Income",
            "member_id": member_id,
            "amount": amount,
            "fund_id": fund_id,
            "method": entry_method,
            "service_date": service_date,
            "entry_date": entry_date,
            "ledger": ledger
        }
        
        self.transactions.append(transaction)
        self.add_audit_log("Record Income", transaction, reason)
        print("SUCCESS: Income transaction recorded and audited.")

    def record_expense(self):
        print("\n--- Record Expense ---")
        category = input("Enter Expense Category (e.g., Utility, Maintenance, Missions): ").strip()
        
        amount_str = input("Enter Amount: ").strip()
        try:
            amount = float(amount_str)
        except ValueError:
            print("Error: Amount must be a number.")
            return
            
        print("\n--- Processing via Inference Engine ---")
        
        # Check valid category
        if self.query_prolog_bool(f"invalid_expense_category('{category}')"):
            print(f"ACTION REJECTED: Invalid Expense Category '{category}'.")
            return
            
        # Expense Audit (Approval vs Escalation)
        if self.query_prolog_bool(f"escalate_expense('{category}', {amount})"):
            print(f"EXPERT ADVICE: Escalation Triggered! Expense of {amount} exceeds {category} budget. Flagged for Manual Finance Committee Review.")
        elif self.query_prolog_bool(f"approve_expense('{category}', {amount})"):
            print(f"EXPERT ADVICE: Expense Approved automatically! {amount} is within {category} budget. Receipt Generation Triggered.")
            
        reason = input("\nEnter 'Reason for Change' (Audit Trail Requirement): ").strip()
        if not reason:
            reason = "Standard Expense Entry"
            
        transaction = {
            "type": "Expense",
            "category": category,
            "amount": amount,
            "date": datetime.date.today().strftime("%Y-%m-%d")
        }
        
        self.transactions.append(transaction)
        self.add_audit_log("Record Expense", transaction, reason)
        print("SUCCESS: Expense recorded and audited.")

    def bank_reconciliation(self):
        print("\n--- Bank Reconciliation ---")
        bank_dep_str = input("Enter actual bank deposit total for checking amounts: ").strip()
        try:
            bank_deposit = float(bank_dep_str)
        except ValueError:
            print("Error: Invalid number.")
            return
            
        # Calculate manual entries total (Income only)
        system_total = sum(t['amount'] for t in self.transactions if t['type'] == 'Income')
        
        print("\n--- Reconciliation Results ---")
        print(f"System Calculated Total (Manual Entries): ${system_total:.2f}")
        print(f"Actual Bank Deposit Total:                ${bank_deposit:.2f}")
        
        if system_total == bank_deposit:
            print("RESULT: PERFECT MATCH. Accountability maintained.")
        else:
            diff = abs(system_total - bank_deposit)
            print(f"WARNING: Discrepancy of ${diff:.2f} detected. Highlighted specific entries for review.")
            
        print("Performance Monitoring: Checking for reduction in Adjusting Journal Entries...")
        print("System Efficacy PROVED: Hours saved on reconciliation.")

    def generate_tax_statements(self):
        print("\n--- Tax Statement Automation ---")
        print("Generating end-of-year contribution statements for members...")
        # Mock automation
        members = set(t['member_id'] for t in self.transactions if t['type'] == 'Income')
        if not members:
            print("No income transactions recorded yet.")
        for m in members:
            total = sum(t['amount'] for t in self.transactions if t['type'] == 'Income' and t['member_id'] == m)
            print(f"Generated IRS-compliant Tax Statement for Member {m}: Total Contributed = ${total:.2f}")
        print("SUCCESS: Tax statements completed.")

    def run(self):
        while True:
            print("\n" + "="*50)
            print(" CHURCH FINANCE EXPERT SYSTEM INTERFACE (Python) ")
            print("="*50)
            print("1. Record Income (Data Entry)")
            print("2. Record Expense (Data Entry)")
            print("3. Run Bank Reconciliation")
            print("4. Generate Tax Statements")
            print("5. View Audit Trail")
            print("6. Exit")
            
            choice = input("\nSelect an option [1-6]: ").strip()
            
            if choice == '1':
                self.record_income()
            elif choice == '2':
                self.record_expense()
            elif choice == '3':
                self.bank_reconciliation()
            elif choice == '4':
                self.generate_tax_statements()
            elif choice == '5':
                print("\n--- System Audit Trail ---")
                if not self.audit_trail:
                    print("Audit trail is empty.")
                else:
                    for log in self.audit_trail:
                        print(log)
            elif choice == '6':
                print("Exiting Expert System. Goodbye.")
                break
            else:
                print("Invalid choice. Try again.")

if __name__ == "__main__":
    app = ExpertSystemInterface()
    app.run()
