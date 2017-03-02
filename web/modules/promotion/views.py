from flask import abort, request, render_template, redirect, url_for, flash, session
from flask_login import login_required, current_user

from web import db
from web.modules.promotion import bp
from web.modules.promotion.forms import CreatePromotionForm

@bp.route('/business/<business_id>/create-promotion', methods=['GET', 'POST'])
@login_required
def create_promotion(business_id):
    form = CreatePromotionForm()
    business = db.business.get_by_id(business_id)
    if not business:
        abort(500)

    if form.validate_on_submit():
        promotion = db.promotion.create_sumo_promotion(business.id, **form.flat_data)
        return redirect(url_for('promotion.view_promotion', promotion_id=promotion.id))

    return render_template('promotion/create.html', form=form, business=business)

@bp.route('/promotion/<promotion_id>')
def view_promotion(promotion_id):
    promotion = db.promotion.get_sumo_promotion_by_id(promotion_id)
    if not promotion:
        abort(500)
    return render_template('promotion/view.html', promotion=promotion)

@bp.route('/promotion/<promotion_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_promotion(promotion_id):
    return render_template('promotion/edit.html')

@bp.route('/promotion/<promotion_id>/delete', methods=['GET', 'DELETE'])
@login_required
def delete_promotion(promotion_id):
    try:
        db.promotion.delete_sumo_promotion_by_id(promotion_id)
    except:
        abort(500)
    return render_template('promotion/delete.html', promotion_id=promotion_id)
    
    
