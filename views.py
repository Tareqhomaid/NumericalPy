from flask import Blueprint, request, render_template, flash
from models import Solver

views = Blueprint('views', __name__)


@views.route('/', methods=['GET'])
def index():
    return render_template('base.html')


@views.route('/calculate', methods=['GET', 'POST'])
def calculate():
    if request.method == 'POST':
        method = ''
        x_val = ''
        result = ''
        f = request.form['value']
        try:
            a = float(request.form['a']) if request.form['a'] else None
            b = float(request.form['b']) if request.form['b'] else None
            x0 = float(request.form['x0']) if request.form['x0'] else None
            c = float(request.form['c']) if request.form['c'] else None
            d = float(request.form['d']) if request.form['d'] else None
            p0 = float(request.form['p0']) if request.form['p0'] else None
        except ValueError:
            flash("Invalid value")
            a, b, c, d, x0, p0 = 0, 0, 0, 0, 0, 0
        solve = Solver(f, a, b, c, d, x0, p0)
        try:
            if a and b:
                result, x_val = solve.bisection()
                method = 'bisection'
            elif x0:
                result, x_val = solve.fixedpoint()
                method = 'fixedpoint'
            elif c and d:
                result, x_val = solve.false_position()
                method = 'False poistion'
            elif p0:
                result, x_val = solve.newton_raphson()
                method = 'Newton Raphson'
            else:
                flash('No values')
        except ValueError:
            flash("Value Error, Try another function?")
        return render_template('result.html', result=result, x_val=x_val, method=method)
    return render_template('base.html')
