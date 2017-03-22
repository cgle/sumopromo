from flask import abort, request, render_template, redirect, url_for, flash, session
from flask_login import login_required, current_user

from web import db
from web.modules.promotion import bp
from web.modules.promotion.forms import PromotionForm, InternetDealForm

@bp.route('/manage-promotions')
@login_required
def manage_promotions():
    promotions = db.promotion.get_promotions_by_merchant(current_user)
    return render_template('promotion/manage-promotions.html', promotions=promotions)

############################
#                          #
# SUMO PROMOTIONS ROUTES   #
#                          #
############################

@bp.route('/create-promotion', methods=['GET', 'POST'])
@login_required
def create_promotion():
    form = PromotionForm()
    if form.validate_on_submit():
        data = form.flat_data
        business_id = data.pop('business_id')
        promotion = db.promotion.create_sumo_promotion(business_id, **data)
        return redirect(url_for('promotion.manage_promotions'))

    return render_template('promotion/sumo-promotion/create.html', form=form)

@bp.route('/biz/<business_id>/create-promotion', methods=['GET', 'POST'])
@login_required
def create_promotion_per_business(business_id):
    business = db.business.get_by_id(business_id)
    form = PromotionForm(business=business)
    if not business:
        abort(500)

    if form.validate_on_submit():
        promotion = db.promotion.create_sumo_promotion(**form.flat_data)
        return redirect(url_for('promotion.manage_promotions'))

    return render_template('promotion/sumo-promotion/create-per-business.html', form=form, business=business)

@bp.route('/promos/<promotion_id>')
def view_promotion(promotion_id):
    promotion = db.promotion.get_sumo_promotion_by_id(promotion_id)
    if not promotion:
        abort(500)
    return render_template('promotion/sumo-promotion/view.html', promotion=promotion)

@bp.route('/promos/<promotion_id>/analytics')
@login_required
def promotion_analytics(promotion_id):
    promotion = db.promotion.get_sumo_promotion_by_id(promotion_id)
    if not promotion:
        abort(500)
    return render_template('promotion/sumo-promotion/analytics.html', promotion=promotion)

@bp.route('/promos/<promotion_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_promotion(promotion_id):
    promotion = db.promotion.get_sumo_promotion_by_id(promotion_id)
    if not promotion:
        abort(500)
    form = PromotionForm(obj=promotion, business=promotion.business)
    if form.validate_on_submit():
        db.promotion.update_one(promotion, **form.flat_data)
        return redirect(url_for('promotion.manage_promotions'))

    return render_template('promotion/sumo-promotion/edit.html', promotion=promotion, form=form)

@bp.route('/promos/<promotion_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_promotion(promotion_id):
    if request.method == 'POST':
        try:
            db.promotion.delete_sumo_promotion_by_id(promotion_id)
        except:
            abort(500)
        return redirect(url_for('promotion.manage_promotions'))

    promotion = db.promotion.get_sumo_promotion_by_id(promotion_id)
    return render_template('promotion/sumo-promotion/delete.html', promotion=promotion)

@bp.route('/promos/<promotion_id>/activate', methods=['GET', 'POST'])
@login_required
def activate_promotion(promotion_id):
    if request.method == 'POST':
        try:
            db.promotion.activate_sumo_promotion(promotion_id)
            return redirect(url_for('promotion.manage_promotions'))
        except:
            abort(500)        
    promotion = db.promotion.get_sumo_promotion_by_id(promotion_id)
    return render_template('promotion/sumo-promotion/activation.html', action='activate', promotion=promotion)

@bp.route('/promos/<promotion_id>/deactivate', methods=['GET', 'POST'])
@login_required
def deactivate_promotion(promotion_id):
    if request.method == 'POST':
        try:
            db.promotion.deactivate_sumo_promotion(promotion_id)
            return redirect(url_for('promotion.manage_promotions'))
        except:
            abort(500)
    promotion = db.promotion.get_sumo_promotion_by_id(promotion_id)
    return render_template('promotion/sumo-promotion/activation.html', action='deactivate', promotion=promotion)

@bp.route('/promos/<promotion_id>/view-claims')
@login_required
def view_promotion_claims(promotion_id):
    return render_template('promotion/sumo-promotion/view-claims.html')

@bp.route('/promos/<promotion_id>/claim', methods=['POST'])
@login_required
def claim_promotion(promotion_id):
    promotion = db.promotion.get_sumo_promotion_by_id(promotion_id)
    voucher = None

    if not promotion:
        abort(500)

    try:
        voucher = db.sumo_voucher.create_per_user(current_user, promotion)
    except:
        abort(500)

    return redirect(url_for('sumo_voucher.view_voucher', voucher_id=voucher.id))

##########################
#                        #
# INTERNET DEAL ROUTES   #
#                        #
##########################

@bp.route('/link-internet-deal', methods=['GET', 'POST'])
@login_required
def link_deal():
    form = InternetDealForm()
    if form.validate_on_submit():
        promotion = db.promotion.create_internet_deal(**form.flat_data)
        return redirect(url_for('promotion.manage_promotions'))

    return render_template('promotion/internet-deal/link.html', form=form)

@bp.route('/biz/<business_id>/link-internet-deal', methods=['GET', 'POST'])
@login_required
def link_deal_per_business(business_id):
    business = db.business.get_by_id(business_id)
    form = InternetDealForm(business=business)
    if not business:
        abort(500)

    if form.validate_on_submit():
        promotion = db.promotion.create_internet_deal(**form.flat_data)
        return redirect(url_for('promotion.manage_promotions'))

    return render_template('promotion/internet-deal/link-per-business.html', form=form, business=business)

@bp.route('/deals/<promotion_id>')
def view_deal(promotion_id):
    promotion = db.promotion.get_internet_deal_by_id(promotion_id)
    if not promotion:
        abort(500)
    return render_template('promotion/internet-deal/view.html', promotion=promotion)

@bp.route('/deals/<promotion_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_deal(promotion_id):
    promotion = db.promotion.get_internet_deal_by_id(promotion_id)
    if not promotion:
        abort(500)

    form = InternetDealForm(obj=promotion, business=promotion.business)
    if form.validate_on_submit():
        db.promotion.update_one(promotion, **form.flat_data)
        return redirect(url_for('promotion.manage_promotions'))

    return render_template('promotion/internet-deal/edit.html', promotion=promotion, form=form)

@bp.route('/deals/<promotion_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_deal(promotion_id):
    if request.method == 'POST':
        try:
            db.promotion.delete_internet_deal_by_id(promotion_id)
        except:
            abort(500)
        return redirect(url_for('promotion.manage_promotions'))

    promotion = db.promotion.get_internet_deal_by_id(promotion_id)
    return render_template('promotion/internet-deal/delete.html', promotion=promotion)

@bp.route('/deals/<promotion_id>/claimers')
@login_required
def view_deal_claims(promotion_id):
    return render_template('promotion/internet-deal/view-claims.html')

@bp.route('/deals/<promotion_id>/claim', methods=['POST'])
@login_required
def claim_deal(promotion_id):
    return 'OK', 200
