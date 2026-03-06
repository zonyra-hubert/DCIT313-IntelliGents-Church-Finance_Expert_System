# Knowledge Engineering Report

## Objective

To map human expertise in church financial management into a logical symbol system (SWI-Prolog and Python) that can accurately reason under uncertainty.

## Knowledge Sources

Knowledge engineering requires translating qualitative expertise from domain specialists into formalized rules. For this system, the primary sources of knowledge were:

1. **Financial Management Principles:** General accounting practices (e.g., restricted vs. unrestricted funds, general ledger posting).
2. **System Constraints Documentation:** Historical transaction analysis requirements (tracking anomalies up to 500% over a 12-month average).
3. **Budgetary Rules & Roles:** Standard operational procedures for expense escalation and committee approval processes.

## Translation to Logic (Mapping Perceptions to Actions)

The Knowledge Base (`knowledge_base/finance_rules.pl`) separates "Intelligence" from the application UI, avoiding hard-coded boolean if-else chains in Python by delegating constraint checking to PROLOG.

### 1. Pattern Recognition

_Human Expert Rule:_ "If someone gives 5 times their usual amount, verify the transaction to prevent manual 0-key errors."
_Prolog Formulation:_

```prolog
needs_verification(MemberID, Amount) :-
    member(MemberID, _, Avg),
    Threshold is Avg * 5,
    Amount > Threshold.
```

### 2. Constraint Satisfaction

_Human Expert Rule:_ "We cannot put money into a closed fund or a fund that doesn't exist."
_Prolog Formulation:_

```prolog
valid_fund(FundID) :- fund(FundID, _, _, open).
invalid_fund(FundID) :- \+ valid_fund(FundID).
```

### 3. Member Status Logic

_Human Expert Rule:_ "If a guest gives a regular tithe, they are likely a new regular attender. Create a profile for them."
_Prolog Formulation:_

```prolog
requires_new_member_profile(MemberID, FundID) :-
    MemberID = guest,
    fund(FundID, 'General Tithe', _, _).
```

### 4. Expense Auditing & Approvals

_Human Expert Rule:_ "Approve normal expenses. If someone wants to spend more than the budget allows, flag it for the committee."
_Prolog Formulation:_

```prolog
approve_expense(Category, Amount) :-
    budget(Category, Allocated),
    Amount =< Allocated.

escalate_expense(Category, Amount) :-
    budget(Category, Allocated),
    Amount > Allocated.
```

## System Integrity Check

The system correctly handles positive and negative tests:

- **Positive Test Case:** Inputting `$600` for a member (`m001`) with a `$100` average successfully triggers the `needs_verification` rule.
- **Negative Test Case:** Intentionally attempting to route income to a non-existent fund identifier fails gracefully, explicitly rejecting the input due to the `invalid_fund` Prolog rule failure.
