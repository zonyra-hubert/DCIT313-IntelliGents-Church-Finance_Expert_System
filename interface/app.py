import sys
import os
import datetime

try:
    from pyswip import Prolog
except ImportError:
    print("Error: The 'pyswip' library is not installed.")
    print("Please install it using: pip install pyswip")
    sys.exit(1)

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = 'church_finance_expert_system_secret_key'

# Global instance of the expert system
expert_system = None

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
        
    def record_income(self, member_id, amount, fund_id, entry_method, service_date, reason=""):
        messages = []
        
        # 1. Constraint Satisfaction
        if self.query_prolog_bool(f"invalid_fund('{fund_id}')"):
            messages.append(f"ACTION REJECTED: Constraint Satisfaction failed. Fund '{fund_id}' does not exist or is closed.")
            return False, messages
        
        # 2. Member Status Logic
        if self.query_prolog_bool(f"requires_new_member_profile('{member_id}', '{fund_id}')"):
            messages.append("EXPERT ADVICE: Member Status Logic triggered. Guest is giving a General Tithe. Please prompt user to create a new member profile.")
            
        # 3. Pattern Recognition (Anomaly Detection)
        if self.query_prolog_bool(f"needs_verification('{member_id}', {amount})"):
            messages.append(f"EXPERT ADVICE: Pattern Recognition triggered. Amount {amount} exceeds 500% of 12-month average for member '{member_id}'. VERIFICATION NEEDED.")
            
        # 4. Financial Routing
        route_query = list(self.prolog.query(f"route_income('{fund_id}', Ledger)"))
        if route_query:
            ledger = route_query[0]['Ledger']
            messages.append(f"FINANCIAL ROUTING: Income routed to => {ledger}")
        else:
            ledger = "Unknown Ledger"
            messages.append("FINANCIAL ROUTING: Could not determine ledger.")
        
        if not reason:
            reason = "Standard Data Entry"
            
        entry_datetime = datetime.datetime.now()
        entry_date = entry_datetime.strftime("%Y-%m-%d")
        entry_time = entry_datetime.strftime("%H:%M:%S")
        
        transaction = {
            "type": "Income",
            "member_id": member_id,
            "amount": amount,
            "fund_id": fund_id,
            "method": entry_method,
            "service_date": service_date,
            "entry_date": entry_date,
            "entry_time": entry_time,
            "ledger": ledger
        }
        
        self.transactions.append(transaction)
        self.add_audit_log("Record Income", transaction, reason)
        messages.append("SUCCESS: Income transaction recorded and audited.")
        return True, messages

    def record_expense(self, category, amount, reason=""):
        messages = []
        
        # Check valid category
        if self.query_prolog_bool(f"invalid_expense_category('{category}')"):
            messages.append(f"ACTION REJECTED: Invalid Expense Category '{category}'.")
            return False, messages
            
        # Expense Audit (Approval vs Escalation)
        if self.query_prolog_bool(f"escalate_expense('{category}', {amount})"):
            messages.append(f"EXPERT ADVICE: Escalation Triggered! Expense of {amount} exceeds {category} budget. Flagged for Manual Finance Committee Review.")
        elif self.query_prolog_bool(f"approve_expense('{category}', {amount})"):
            messages.append(f"EXPERT ADVICE: Expense Approved automatically! {amount} is within {category} budget. Receipt Generation Triggered.")
            
        if not reason:
            reason = "Standard Expense Entry"

        now = datetime.datetime.now()
        transaction = {
            "type": "Expense",
            "category": category,
            "amount": amount,
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S")
        }
        
        self.transactions.append(transaction)
        self.add_audit_log("Record Expense", transaction, reason)
        messages.append("SUCCESS: Expense recorded and audited.")
        return True, messages

    def bank_reconciliation(self, bank_deposit):
        # Calculate manual entries total (Income only)
        system_total = sum(t['amount'] for t in self.transactions if t['type'] == 'Income')
        
        result = {
            "system_total": system_total,
            "bank_deposit": bank_deposit,
            "match": system_total == bank_deposit,
            "difference": abs(system_total - bank_deposit) if system_total != bank_deposit else 0
        }
        
        return result

    def generate_tax_statements(self):
        members = set(t['member_id'] for t in self.transactions if t['type'] == 'Income')
        statements = []
        
        if not members:
            return []
            
        for m in members:
            total = sum(t['amount'] for t in self.transactions if t['type'] == 'Income' and t['member_id'] == m)
            statements.append({
                "member_id": m,
                "total_contributed": total
            })
        
        return statements

# Flask Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/record_income', methods=['GET', 'POST'])
def record_income():
    if request.method == 'POST':
        member_id = request.form.get('member_id')
        amount = float(request.form.get('amount'))
        fund_id = request.form.get('fund_id')
        entry_method = request.form.get('entry_method')
        service_date = request.form.get('service_date')
        reason = request.form.get('reason', '')
        
        success, messages = expert_system.record_income(member_id, amount, fund_id, entry_method, service_date, reason)
        
        if success:
            flash('Income recorded successfully!', 'success')
        else:
            flash('Failed to record income.', 'error')
            
        return render_template('record_income.html', messages=messages)
    
    return render_template('record_income.html')

@app.route('/record_expense', methods=['GET', 'POST'])
def record_expense():
    if request.method == 'POST':
        category = request.form.get('category')
        amount = float(request.form.get('amount'))
        reason = request.form.get('reason', '')
        
        success, messages = expert_system.record_expense(category, amount, reason)
        
        if success:
            flash('Expense recorded successfully!', 'success')
        else:
            flash('Failed to record expense.', 'error')
            
        return render_template('record_expense.html', messages=messages)
    
    return render_template('record_expense.html')

@app.route('/bank_reconciliation', methods=['GET', 'POST'])
def bank_reconciliation():
    if request.method == 'POST':
        bank_deposit = float(request.form.get('bank_deposit'))
        result = expert_system.bank_reconciliation(bank_deposit)
        return render_template('bank_reconciliation.html', result=result)
    
    return render_template('bank_reconciliation.html')

@app.route('/tax_statements')
def tax_statements():
    statements = expert_system.generate_tax_statements()
    return render_template('tax_statements.html', statements=statements)

@app.route('/audit_trail')
def audit_trail():
    return render_template('audit_trail.html', audit_trail=expert_system.audit_trail)

if __name__ == "__main__":
    expert_system = ExpertSystemInterface()
    app.run(debug=True)
