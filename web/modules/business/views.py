from flask import abort, current_app, request, render_template, redirect, url_for, flash, session
from werkzeug import secure_filename

from flask_login import login_required, current_user

from web import db, s3, s3_buckets
from web.modules.business import bp
from web.modules.business.forms import CreateBusinessForm

def is_merchant(business):
    return current_user.id == business.merchant_id

@bp.route('/create-business', methods=['GET', 'POST'])
@login_required
def create_business():
    form = CreateBusinessForm()
    if form.validate_on_submit():
        data = form.flat_data
        logo = data.pop('logo')

        try:
            business = db.business.create(current_user.id, **data)

            # upload logo
            filename = '{}/logo/{}'.format(business.id, secure_filename(logo.filename))
            logo_url = s3.upload_file(logo, filename, s3_buckets['business'])
            db.business.update_one(business, logo=logo_url)
        except:
            raise
            abort(500)
        
        return redirect(url_for('business.view_business', business_id=business.id))

    return render_template('business/create.html', form=form)

@bp.route('/my-businesses')
@login_required
def my_businesses():
    businesses = db.business.get_by_merchant(current_user.id)
    return render_template('account/my-businesses.html', businesses=businesses)

@bp.route('/business/<business_id>')
def view_business(business_id):
    business = db.business.get_by_id(business_id)
    if not business:
        abort(500)
    return render_template('business/view.html', business=business)

@bp.route('/business/<business_id>/edit', methods=['GET','POST'])
@login_required
def edit_business(business_id):
    business = db.business.get_by_id(business_id)

    if not business:
        abort(500)

    if not is_merchant(business):
        abort(403)

    form = CreateBusinessForm(obj=business)

    if form.validate_on_submit():
        data = form.flat_data
        logo = data.pop('logo')
        db.business.update_one(business, **data)
        return redirect(url_for('business.view_business', business_id=business_id))

    form.address.process(None, business)
    form.social.process(None, business)

    return render_template('business/edit.html', form=form, business=business)

@bp.route('/business/<business_id>/delete', methods=['GET','POST'])
@login_required
def delete_business(business_id):
    business = db.business.get_by_id(business_id)
    if not business:
        abort(500)
    
    if not is_merchant(business):
        abort(403)

    if request.method == 'POST':
        db.business.delete_one(business)
        return redirect(url_for('business.my_businesses'))
    return render_template('business/delete.html', business=business)

