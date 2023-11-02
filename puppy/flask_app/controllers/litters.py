from flask_app import app
from flask import render_template,request,redirect,session
from flask_app.models import user,liter

@app.route('/new')
def newLitter():
    return render_template('new.html')


@app.route('/new/litter', methods=['POST'])
def create():
    if not liter.Litters.is_valid(request.form):
        return redirect('/new')
    else:
        data={
            "breed" : request.form['breed'],
            "quantity" : request.form['quantity'],
            "home" : request.form['home'],
            "description" : request.form['description'],
            "user_id" : int(request.form['user_id'])
        }
        liter.Litters.create(data)
    
    return redirect('/dashboard')

@app.route('/view/<int:id>')
def one_litter(id):
    user_from_db = user.User.get_by_id({"id": int(session['logged_in'])})
    user_id = int(session['logged_in'])
    liter_from_db = liter.Litters.get_one({'id':id})
    return render_template('view.html', one_liter = liter_from_db, user_id = user_id, user = user_from_db )

@app.route('/delete/<int:id>')
def delete(id):
    liter.Litters.delete({"id":id})
    return redirect('/dashboard')

@app.route('/update/<int:id>')
def edit(id):
    one_liter=liter.Litters.get_one({"id":id})
    return render_template('edit.html',one_liter=one_liter)

@app.route('/liter/update/<int:id>', methods=['POST'])
def update(id):
    if not liter.Litters.is_valid(request.form):
        return redirect('/update')
    else:
        data={
            "id": id,
            "breed" : request.form['breed'],
            "quantity" : request.form['quantity'],
            "home" : request.form['home'],
            "description" : request.form['description'],
            "user_id" : int(request.form['user_id'])
        }
        liter.Litters.update(data)
    return redirect('/dashboard')