from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# List to store expenses
expenses = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the expense details from the form
        description = request.form.get('description')
        amount = request.form.get('amount')

        if description and amount:
            try:
                amount = float(amount)
                expenses.append({'description': description, 'amount': amount})
                flash('Expense added successfully!', 'success')
            except ValueError:
                flash('Please enter a valid amount.', 'danger')
        else:
            flash('Please fill in all fields.', 'danger')

        return redirect(url_for('index'))

    total_expense = sum(expense['amount'] for expense in expenses)
    return render_template('index.html', expenses=expenses, total_expense=total_expense)

if __name__ == '__main__':
    app.run(debug=True)