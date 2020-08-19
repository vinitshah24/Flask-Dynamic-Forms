from flask import Flask, render_template, request
from wtforms import Form, StringField, BooleanField, FormField, FieldList
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config.from_object('config')
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = "47YX7XCk"


class ResidenceForm(Form):
    place = StringField()
    zipcode = StringField()


class MyForm(Form):
    firstname = StringField()
    lastname = FieldList(StringField(validators=[DataRequired()]), min_entries=1)
    boolean = BooleanField()
    email = FieldList(StringField(), min_entries=1)
    residence = FieldList(FormField(ResidenceForm), min_entries=1)


@app.route('/', methods=["GET", "POST"])
def index():
    firstname = "MyFirstName"
    lastname = "MyLastName"
    form = MyForm()
    form.firstname.data = firstname
    for i in range(1):
        form.lastname.append_entry(lastname)
    form.email.append_entry()
    if request.method == "POST":
        # Get data from AJAX request
        form = MyForm(request.form)
        for fieldlist in form:
            try:
                _ = (entry for entry in fieldlist)
            except TypeError:
                print(fieldlist.name, fieldlist.data)
                continue
            for entry in fieldlist:
                print(entry.name, entry.data)
        # Server-Side Validation
        if form.validate():
            # Valid data -  Can be saved to a database
            return form.data
        else:
            # Validation Failed
            return 'Data not saved!'
    return render_template('form.html', form=form)


if __name__ == '__main__':
    app.run()
