% ==============================================
% FACTS: Knowledge Base of Church Finance
% ==============================================

% member(MemberID, Name, AverageMonthlyGiving).
% AverageMonthlyGiving allows us to calculate 500% threshold for pattern recognition.
member(m001, 'Dave Henderson', 100).
member(m002, 'Alex Yarbo', 500).
member(m003, 'Jumma Akwasi', 50).
member(m004, 'Mavis Davis', 100).
member(m005, 'Boyd Christian', 3000).
member(m006, 'Jason Jacobs', 500).
member(m007, 'Catryn Boison', 250).
member(guest, 'Guest', 700).

% fund(FundID, FundName, Type, Status).
% Type: restricted or unrestricted. Status: open or closed.
fund(f001, 'General Tithe', unrestricted, open).
fund(f002, 'Building Fund', restricted, open).
fund(f003, 'Missions', restricted, open).
fund(f004, 'Youth Trip 2022', restricted, closed).

% budget(Category, AllocatedAmount).
% Budgets for expense auditing.
budget('Utilities', 500).
budget('Maintenance', 1000).
budget('Missions', 2000).
budget('Salaries', 2000).
budget('Marketing', 500).


% ==============================================
% RULES: The Inference Engine (Decision Making)
% ==============================================

% 1. Pattern Recognition (Anomaly Detection):
% Flags entries for "Verification Needed" if an amount exceeds a member's 12-month average by 500% (i.e. > 5 * Avg).
needs_verification(MemberID, Amount) :-
    member(MemberID, _, Avg),
    Threshold is Avg * 5,
    Amount > Threshold.

% 2. Constraint Satisfaction:
% Automatically reject entries coded to non-existent or closed church funds.
valid_fund(FundID) :-
    fund(FundID, _, _, open).

invalid_fund(FundID) :-
    \+ valid_fund(FundID).

% 3. Member Status Logic:
% If a "Tithe" is marked for a "Guest", the system must prompt the user to create a new member profile.
requires_new_member_profile(MemberID, FundID) :-
    MemberID = guest,
    fund(FundID, 'General Tithe', _, _).

% 4. Expense Audit:
% For every expense, the system must check if it exceeds the allocated budget category.
exceeds_budget(Category, Amount) :-
    budget(Category, Allocated),
    Amount > Allocated.

invalid_expense_category(Category) :-
    \+ budget(Category, _).

% ==============================================
% RULES: Financial Routing & Ledger Management
% ==============================================

% Income Routing (Restricted & General):
% Direct data to the correct accounting destination based on Fund Type.
route_income(FundID, Ledger) :-
    fund(FundID, _, Type, _),
    (Type = restricted -> Ledger = 'Restricted Ledger' ; Type = unrestricted -> Ledger = 'General Ledger').

% Expense Approval:
% Automatically approve expenses if they fall within budget.
approve_expense(Category, Amount) :-
    budget(Category, Allocated),
    Amount =< Allocated.

% Escalation:
% Flag any expense exceeding budget limits for manual Finance Committee Review.
escalate_expense(Category, Amount) :-
    exceeds_budget(Category, Amount).
