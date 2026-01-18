"""
SlipOK API Utility Module
ตรวจสอบสลิปการโอนเงินผ่าน SlipOK API
"""
import requests
import json
from io import BytesIO

# SlipOK API Configuration
SLIPOK_API_URL = "https://api.slipok.com/api/line/apikey/59362"
SLIPOK_API_KEY = "SLIPOK67Q1ZBM"


def verify_slip(image_data, expected_amount=None):
    """
    ตรวจสอบสลิปการโอนเงินกับ SlipOK API
    
    Args:
        image_data: ไฟล์รูปสลิป (bytes หรือ file-like object)
        expected_amount: ยอดเงินที่คาดหวัง (optional)
    
    Returns:
        dict: ผลลัพธ์การตรวจสอบ
        {
            "success": True/False,
            "data": {...},  # ข้อมูลจาก API
            "amount": float,  # ยอดเงิน
            "transaction_ref": str,  # เลขอ้างอิง
            "sender": {...},  # ข้อมูลผู้โอน
            "receiver": {...},  # ข้อมูลผู้รับ
            "error_code": int,  # รหัสข้อผิดพลาด (ถ้ามี)
            "error_message": str  # ข้อความข้อผิดพลาด (ถ้ามี)
        }
    """
    try:
        headers = {
            "x-authorization": SLIPOK_API_KEY
        }
        
        # Prepare file for upload
        if isinstance(image_data, bytes):
            files = {
                "files": ("slip.jpg", BytesIO(image_data), "image/jpeg")
            }
        else:
            files = {
                "files": ("slip.jpg", image_data, "image/jpeg")
            }
        
        # Optional: Add amount for verification
        data = {"log": True}
        if expected_amount:
            data["amount"] = expected_amount
        
        # Send request to SlipOK API
        response = requests.post(
            SLIPOK_API_URL,
            headers=headers,
            files=files,
            data=data,
            timeout=30
        )
        
        result = response.json()
        
        # Check if verification was successful
        if response.status_code == 200 and result.get("success", False):
            slip_data = result.get("data", {})
            
            # Handle amount - could be dict or direct value
            amount_data = slip_data.get("amount", 0)
            if isinstance(amount_data, dict):
                amount = float(amount_data.get("amount", 0))
            else:
                amount = float(amount_data) if amount_data else 0
            
            return {
                "success": True,
                "data": result,
                "amount": amount,
                "transaction_ref": slip_data.get("transRef", ""),
                "sender": {
                    "name": slip_data.get("sender", {}).get("displayName", ""),
                    "account": slip_data.get("sender", {}).get("account", {}).get("value", "") if isinstance(slip_data.get("sender", {}).get("account"), dict) else slip_data.get("sender", {}).get("account", "")
                },
                "receiver": {
                    "name": slip_data.get("receiver", {}).get("displayName", ""),
                    "account": slip_data.get("receiver", {}).get("account", {}).get("value", "") if isinstance(slip_data.get("receiver", {}).get("account"), dict) else slip_data.get("receiver", {}).get("account", "")
                },
                "transfer_date": slip_data.get("transDate", ""),
                "bank": slip_data.get("receivingBank", "")
            }
        else:
            # Handle error codes
            error_code = result.get("code", 0)
            error_messages = {
                1007: "QR Code หมดอายุหรือไม่พบธุรกรรม",
                1010: "ธนาคารมีความล่าช้า กรุณาลองใหม่อีกครั้ง",
                1012: "สลิปนี้เคยถูกใช้งานแล้ว (ซ้ำ)",
                1013: "ยอดเงินไม่ตรงกับที่ระบุ",
                1014: "ผู้รับเงินไม่ถูกต้อง"
            }
            
            return {
                "success": False,
                "error_code": error_code,
                "error_message": error_messages.get(error_code, result.get("message", "ไม่สามารถตรวจสอบสลิปได้")),
                "data": result
            }
            
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error_code": 0,
            "error_message": "การเชื่อมต่อ SlipOK หมดเวลา กรุณาลองใหม่"
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error_code": 0,
            "error_message": f"เกิดข้อผิดพลาดในการเชื่อมต่อ: {str(e)}"
        }
    except json.JSONDecodeError:
        return {
            "success": False,
            "error_code": 0,
            "error_message": "ไม่สามารถอ่านผลลัพธ์จาก SlipOK ได้"
        }
    except Exception as e:
        return {
            "success": False,
            "error_code": 0,
            "error_message": f"เกิดข้อผิดพลาด: {str(e)}"
        }


def verify_slip_url(image_url, expected_amount=None):
    """
    ตรวจสอบสลิปจาก URL
    
    Args:
        image_url: URL ของรูปสลิป
        expected_amount: ยอดเงินที่คาดหวัง (optional)
    
    Returns:
        dict: ผลลัพธ์การตรวจสอบ (เหมือน verify_slip)
    """
    try:
        headers = {
            "x-authorization": SLIPOK_API_KEY
        }
        
        data = {
            "url": image_url,
            "log": True
        }
        
        if expected_amount:
            data["amount"] = expected_amount
        
        response = requests.post(
            SLIPOK_API_URL,
            headers=headers,
            data=data,
            timeout=30
        )
        
        result = response.json()
        
        if response.status_code == 200 and result.get("success", False):
            slip_data = result.get("data", {})
            
            # Handle amount - could be dict or direct value
            amount_data = slip_data.get("amount", 0)
            if isinstance(amount_data, dict):
                amount = float(amount_data.get("amount", 0))
            else:
                amount = float(amount_data) if amount_data else 0
            
            return {
                "success": True,
                "data": result,
                "amount": amount,
                "transaction_ref": slip_data.get("transRef", ""),
                "sender": {
                    "name": slip_data.get("sender", {}).get("displayName", ""),
                    "account": slip_data.get("sender", {}).get("account", {}).get("value", "") if isinstance(slip_data.get("sender", {}).get("account"), dict) else slip_data.get("sender", {}).get("account", "")
                },
                "receiver": {
                    "name": slip_data.get("receiver", {}).get("displayName", ""),
                    "account": slip_data.get("receiver", {}).get("account", {}).get("value", "") if isinstance(slip_data.get("receiver", {}).get("account"), dict) else slip_data.get("receiver", {}).get("account", "")
                },
                "transfer_date": slip_data.get("transDate", ""),
                "bank": slip_data.get("receivingBank", "")
            }
        else:
            error_code = result.get("code", 0)
            error_messages = {
                1007: "QR Code หมดอายุหรือไม่พบธุรกรรม",
                1010: "ธนาคารมีความล่าช้า กรุณาลองใหม่อีกครั้ง",
                1012: "สลิปนี้เคยถูกใช้งานแล้ว (ซ้ำ)",
                1013: "ยอดเงินไม่ตรงกับที่ระบุ",
                1014: "ผู้รับเงินไม่ถูกต้อง"
            }
            
            return {
                "success": False,
                "error_code": error_code,
                "error_message": error_messages.get(error_code, result.get("message", "ไม่สามารถตรวจสอบสลิปได้")),
                "data": result
            }
            
    except Exception as e:
        return {
            "success": False,
            "error_code": 0,
            "error_message": f"เกิดข้อผิดพลาด: {str(e)}"
        }
