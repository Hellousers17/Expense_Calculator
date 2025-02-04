from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# List to store expenses
expenses = []

users = {}

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


@app.route('/expenses', methods=['GET', 'POST'])

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
    app.run()