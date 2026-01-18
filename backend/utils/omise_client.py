import omise
import os
from config import Config

# ===== ตั้งค่า API Key =====
omise.api_secret = os.getenv("OMISE_SECRET_KEY", Config.OMISE_SECRET_KEY)
omise.api_public = os.getenv("OMISE_PUBLIC_KEY", Config.OMISE_PUBLIC_KEY)

class OmiseClient:
    @staticmethod
    def create_charge_promptpay(amount, return_uri=None):
        """
        ✅ สร้าง PromptPay Charge
        amount: int (หน่วยเป็นบาท)
        return_uri: URL ที่จะให้ Omise Redirect กลับหลังจ่ายสำเร็จ
        """
        try:
            charge = omise.Charge.create(
                amount=amount * 100,  # แปลงเป็น สตางค์
                currency=Config.OMISE_CURRENCY,
                source={"type": "promptpay"},
                return_uri=return_uri or Config.OMISE_RETURN_URL
            )
            return {"status": "success", "data": charge}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def create_charge_credit(amount, card_token, return_uri=None):
        """
        ✅ สร้าง Charge สำหรับบัตรเครดิต/เดบิต
        card_token: token ที่ Frontend ส่งมาจาก Omise.js
        """
        try:
            charge = omise.Charge.create(
                amount=amount * 100,
                currency=Config.OMISE_CURRENCY,
                card=card_token,
                return_uri=return_uri or Config.OMISE_RETURN_URL
            )
            return {"status": "success", "data": charge}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def retrieve_charge(charge_id):
        """
        ✅ ใช้ดึงสถานะของ Charge จาก Omise
        charge_id: id ของการชำระเงิน เช่น chrg_test_xxxxxxx
        """
        try:
            charge = omise.Charge.retrieve(charge_id)
            return {"status": "success", "data": charge}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def is_charge_success(charge_data):
        """
        ✅ ตรวจสอบว่า Payment สำเร็จหรือไม่
        """
        try:
            return charge_data.get('data') and charge_data['data'].status == 'successful'
        except Exception:
            return False
