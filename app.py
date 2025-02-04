from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# List to store expenses
expenses = []

# In-memory user storage (for demonstration purposes)
users = {}

# Budget limits
budget_limits = {
    'daily': None,
    'weekly': None,
    'monthly': None
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in users and users[username] == password:
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in users:
            flash('Username already exists.', 'danger')
        else:
            users[username] = password
            flash('Sign up successful! You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/set_budget', methods=['GET', 'POST'])
def budget_settings():
    if request.method == 'POST':
        daily_budget = request.form.get('daily_budget')
        weekly_budget = request.form.get('weekly_budget')
        monthly_budget = request.form.get('monthly_budget')

        global budget_limits
        budget_limits['daily'] = float(daily_budget) if daily_budget else None
        budget_limits['weekly'] = float(weekly_budget) if weekly_budget else None
        budget_limits['monthly'] = float(monthly_budget) if monthly_budget else None

        flash('Budget limits set successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('budget_settings.html', budget_limits=budget_limits)

@app.route('/expense', methods=['GET', 'POST'])
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

    # Check if budget is exceeded
    budget_exceeded = False
    if budget_limits['daily'] is not None and total_expense > budget_limits['daily']:
        budget_exceeded = True
    elif budget_limits['weekly'] is not None and total_expense > budget_limits['weekly']:
        budget_exceeded = True
    elif budget_limits['monthly'] is not None and total_expense > budget_limits['monthly']:
        budget_exceeded = True

    return render_template('index.html', expenses=expenses, total_expense=total_expense, budget_exceeded=budget_exceeded)

if __name__ == '__main__':
    app.run(debug=True)