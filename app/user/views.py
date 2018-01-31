from flask import flash, redirect, render_template, url_for, request, current_app as app
from flask_login import login_required, current_user

from . import user
from forms import UserUpdateForm, NoteForm
from .. import db
from ..models import User, Career, Note, Redis


@user.route('/viewprofile', methods=['GET', 'POST'])
@login_required
def viewprofile():
    """
    Handle requests to the /register route
    Add an notetaker to the database through the registration form
    """
    user = current_user
    form = UserUpdateForm(obj=user)
    form.populate_obj(user)
    if form.validate_on_submit():
        form.populate_obj(user)

        db.session.commit()

        flash('You have successfully edited your profile!')
    return render_template('user/user.html', title="View Profile",
                           user=user, form=form, action='Edit')


@user.route('/notes')
@login_required
# @app.cache.cached(timeout=50)
def list_notes():
    """
    List all roles
    """
    user = current_user
    try:
        notes = user.notes
    except BaseException, e:
        notes = False

    return render_template('user/notes.html', user=user,
                           notes=notes, title='Notes')


@user.route('/notes/add', methods=['GET', 'POST'])
@login_required
def add_note():
    """
    Add a role to the database
    """
    curr_app = app._get_current_object()

    redis_conn = Redis.new_connection(curr_app.config)

    add_note = True
    user = current_user
    form = NoteForm()

    bol = form.validate_on_submit()
    if bol:
        note = Note(title=form.title.data,
                    body=form.body.data)

        key = "data-cached:notes-title-%s" % (note.title)
        tmp_note = Redis.get_data(redis_conn, key)

        try:
            # add role to the database
            user.notes.append(note)
            db.session.add(note)
            db.session.commit()
            Redis.set_data(redis_conn, key, note)
            flash('You have successfully added a new note to the user.')
        except BaseException, e:
            # in case role name already exists
            db.session.rollback()
            flash('Error: .')
        finally:
            db.session.close()
        # redirect to the roles page
        response = redirect(url_for('user.list_notes'))
    else:
        # load role template
        response = render_template('user/note.html', add_role=add_note,
                                   form=form, title='Add Note')
    return response


@user.route('/notes/trans', methods=['GET', 'POST'])
def method_a():
    '''
    transaction demo
    :return:
    '''
    connection = db.engine.connect()
    trans = connection.begin()
    try:
        connection.execute("insert into notes(title,user_id,body) values ('bat_004', 1, 'lala')")
        method_b(connection)
        trans.commit()
    except BaseException, e:
        trans.rollback()
        raise
    return 'ok'


def method_b(connection):
    trans = connection.begin()
    try:
        connection.execute("insert into notes(title,user_id,body) values ('bat_104', 1, 'lala')")
        connection.execute("insert into notes(title,user_id,body) values ('bat_204', 1, 'lala')")
        trans.commit()
    except BaseException, e:
        trans.rollback()
        raise


@user.route('/notes/trans_1', methods=['GET', 'POST'])
def method_a_1():
    '''
    transaction demo
    :return:
    '''
    note = Note(title=None, body=None)
    note.title = 'abc-001'
    note.body = 'xyz--001'
    note.user_id = 1
    try:
        db.session.add(note)
        method_b_1()
        db.session.commit()
    except BaseException, e:
        raise
    return 'ok'


def method_b_1():
    note = Note(title=None, body=None)
    note.title = 'abc-100'
    note.body = 'xyz--100'
    note.user_id = 1
    try:
        db.session.add(note)
        db.session.commit()
    except BaseException, e:
        raise


@user.route('/notes/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_note(id):
    """
    Edit a role
    """
    add_note = False
    note = Note.query.get_or_404(id)
    form = NoteForm(obj=note)
    if form.validate_on_submit():
        note.title = form.title.data
        note.body = form.body.data
        db.session.add(note)
        db.session.commit()
        flash('You have successfully edited the note.')

        # redirect to the roles page
        return redirect(url_for('user.list_notes'))

    form.body.data = note.body
    form.title.data = note.title
    return render_template('user/note.html', add_role=add_note,
                           form=form, title="Edit Note")


@user.route('/notes/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_note(id):
    """
    Delete a role from the database
    """

    note = Note.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    flash('You have successfully deleted the role.')

    # redirect to the roles page
    return redirect(url_for('user.list_notes'))

    return render_template(title="Delete Note")
