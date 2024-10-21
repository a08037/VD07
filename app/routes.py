from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db, bcrypt
from app.forms import UpdateProfileForm


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        # Обновление имени пользователя и почты
        current_user.username = form.username.data
        current_user.email = form.email.data

        # Проверка и обновление пароля, если он был изменён
        if form.password.data:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            current_user.password = hashed_password

        db.session.commit()
        flash('Ваш профиль был обновлен!', 'success')
        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template('account.html', title='Account', form=form)
