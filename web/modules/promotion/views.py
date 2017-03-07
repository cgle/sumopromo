from flask import abort, request, render_template, redirect, url_for, flash, session
from flask_login import login_required, current_user

from web import db
from web.modules.promotion import bp
from web.modules.promotion.forms import CreatePromotionForm, EditPromotionForm

@bp.route('/business/<business_id>/create-promotion', methods=['GET', 'POST'])
@login_required
def create_promotion(business_id):
    form = CreatePromotionForm()
    business = db.business.get_by_id(business_id)
    if not business:
        abort(500)

    if form.validate_on_submit():
        promotion = db.promotion.create_sumo_promotion(business.id, **form.flat_data)
        return redirect(url_for('promotion.manage_promotions', promotion_id=promotion.id))

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
    promotion = db.promotion.get_sumo_promotion_by_id(promotion_id)
    if not promotion:
        abort(500)
    form = EditPromotionForm(obj=promotion)
    if form.validate_on_submit():
        db.promotion.update_one(promotion, **form.flat_data)
        return redirect(url_for('promotion.manage_promotions'))
    return render_template('promotion/edit.html', promotion=promotion, form=form)

@bp.route('/promotion/<promotion_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_promotion(promotion_id):
    if request.method == 'POST':
        try:
            db.promotion.delete_sumo_promotion_by_id(promotion_id)
        except:
            abort(500)

    promotion = db.promotion.get_sumo_promotion_by_id(promotion_id)
    return render_template('promotion/delete.html', promotion=promotion)

@bp.route('/promotion/<promotion_id>/activate', methods=['GET', 'POST'])
@login_required
def activate_promotion(promotion_id):
    if request.method == 'POST':
        try:
            db.promotion.activate_sumo_promotion(promotion_id)
            return redirect(url_for('promotion.manage_promotions'))
        except:
            abort(500)        
    promotion = db.promotion.get_sumo_promotion_by_id(promotion_id)
    return render_template('promotion/activation.html', action='activate', promotion=promotion)

@bp.route('/promotion/<promotion_id>/deactivate', methods=['GET', 'POST'])
@login_required
def deactivate_promotion(promotion_id):
    if request.method == 'POST':
        try:
            db.promotion.deactivate_sumo_promotion(promotion_id)
            return redirect(url_for('promotion.manage_promotions'))
        except:
            abort(500)
    promotion = db.promotion.get_sumo_promotion_by_id(promotion_id)
    return render_template('promotion/activation.html', action='deactivate', promotion=promotion)

@bp.route('/manage-promotions')
@login_required
def manage_promotions():
    promotions = db.promotion.get_sumo_promotions_by_merchant(current_user)
    return render_template('promotion/manage-promotions.html', promotions=promotions)



