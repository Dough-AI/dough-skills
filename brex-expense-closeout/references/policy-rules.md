TEMPLATE-UNFILLED (delete this line once you have filled in the file)

# Expense policy rules

The skill reads this file before checking expenses. Fill in what your policy says and delete anything it doesn't cover. Each line below is an example of the kind of rule the skill can use, not a recommendation.

Source: link to your expense or card policy (the policy wins over this summary).

## Every transaction

- Receipt: e.g. required for every transaction, or above a set amount. What is accepted when there is none, e.g. a written explanation.
- Memo: e.g. required, stating the business purpose.
- Expense category: the skill uses the categories from Brex (`list_expense_categories`). Add any rule for a catch-all category, e.g. "Other needs a reason in the memo".
- Deadline: e.g. reconciled within N days after month end, and what happens after.

## Card types (for the card fit check)

- e.g. Travel cards: travel spend only, not subscriptions.

## Meal cap (for the meal cap check)

- e.g. a daily cap per person, by country or region if it varies.

## Personal or accidental charges

- Who to tell, and how the cardholder repays.
