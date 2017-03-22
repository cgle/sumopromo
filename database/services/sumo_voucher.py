from database.models import SumoVoucher
from database.services import DBService, DBServiceError
from datetime import datetime

class SumoVoucherDBService(DBService):
    
    name = 'sumo_voucher'
    Model = SumoVoucher

    def create_per_user(self, user, promotion):
        if not promotion.is_sumo:
            raise DBServiceError('Promotion is not a sumo promotion')

        if not promotion.is_live:
            raise DBServiceError('Promotion is not active')

        voucher = self.filter(SumoVoucher.user_id == user.id,
                              SumoVoucher.promotion_id == promotion.id,
                              SumoVoucher.confirmed_at == None)

        if voucher:
            return voucher[0] # filter return a list

        num_vouchers = self.count_per_user(user, promotion)

        if num_vouchers >= promotion.max_quantity_per_person:
            raise DBServiceError('User has already claimed max {} vouchers'.format(promotion.max_quantity_per_person))

        voucher = self.add(user_id=user.id, promotion_id=promotion.id)
        return voucher

    def confirm_voucher(self, voucher):
        if voucher.confirmed_at:
            raise DBServiceError('Voucher is already confirmed at {}'.format(voucher.confirmed_at))
        
        if not voucher.promotion.is_live:
            raise DBServiceError('Promotion is not live')
        
        self.update_one(voucher, confirmed_at=datetime.now())
        return voucher
    
    def get_by_code(self, voucher_code):        
        voucher = self.filter_by(sumo_code=voucher_code)
        if voucher:
            return voucher[0]
        return None

    def count_per_user(self, user, promotion):
        num_vouchers = self.filter_q(SumoVoucher.user_id == user.id,
                                     SumoVoucher.promotion_id == promotion.id).count()

        return num_vouchers

