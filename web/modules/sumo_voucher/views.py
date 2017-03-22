from flask import render_template, request, abort
from flask_login import login_required, current_user

from web import db
from web.modules.sumo_voucher import bp

@bp.route('/vouchers/<voucher_id>')
@login_required
def view_voucher(voucher_id):
    voucher = db.sumo_voucher.get_by_id(voucher_id)
    if voucher is None:
        abort(500)
    return render_template('sumo_voucher/view.html', voucher=voucher)


@bp.route('/confirm-voucher', methods=['GET', 'POST'])
@login_required
def confirm_voucher():
    if request.method == 'POST':        
        voucher_code = request.args.get('code', None)
        voucher_id = request.args.get('id', None)
        
        voucher = (voucher_id is not None and db.sumo_voucher.get_by_id(voucher_id)) or \
                  (voucher_code is not None and db.sumo_voucher.get_by_code(voucher_code))
        
        if not voucher:
            return 'Voucher not found', 500

        try:
            db.sumo_voucher.confirm_voucher(voucher)
        except Exception as e:
            return str(e), 500
            
        return 'Voucher is confirmed!', 200

    return render_template('sumo_voucher/confirm.html')
