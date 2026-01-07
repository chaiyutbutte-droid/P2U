from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from datetime import datetime, timedelta

from models import User, Auction, AuctionBid, Notification, AutoBid

auction = Blueprint('auction', __name__)


# -----------------------------
# Get All Active Auctions
# -----------------------------
@auction.route('/auctions', methods=['GET'])
def get_auctions():
    """Get all active auctions"""
    category = request.args.get('category', 'all')
    
    # Check and end expired auctions
    now = datetime.utcnow()
    expired = Auction.objects(end_time__lt=now, is_ended=False)
    for a in expired:
        end_auction(a)
    
    # Query auctions
    if category == 'all':
        auctions = Auction.objects(is_active=True, is_ended=False).order_by('-created_at')
    else:
        auctions = Auction.objects(is_active=True, is_ended=False, category=category).order_by('-created_at')
    
    result = []
    for a in auctions:
        time_left = (a.end_time - now).total_seconds() if a.end_time > now else 0
        result.append({
            "id": str(a.id),
            "title": a.title,
            "description": a.description,
            "image_url": a.image_url,
            "category": a.category,
            "starting_price": float(a.starting_price),
            "current_price": float(a.current_price),
            "min_bid_increment": float(a.min_bid_increment),
            "total_bids": a.total_bids,
            "time_left": int(time_left),
            "end_time": a.end_time.strftime("%Y-%m-%d %H:%M:%S"),
            "seller": {
                "id": str(a.seller.id),
                "username": a.seller.username,
                "shop_name": a.seller.shop_name
            }
        })
    
    return jsonify({"auctions": result}), 200


# -----------------------------
# Get Single Auction
# -----------------------------
@auction.route('/auctions/<auction_id>', methods=['GET'])
def get_auction(auction_id):
    """Get auction details with full bid history"""
    try:
        a = Auction.objects.get(id=ObjectId(auction_id))
    except:
        return jsonify({"msg": "Auction not found"}), 404
    
    now = datetime.utcnow()
    time_left = (a.end_time - now).total_seconds() if a.end_time > now else 0
    
    # Get ALL bids for this auction (not just 20)
    bids = AuctionBid.objects(auction=a).order_by('-created_at')
    bid_history = []
    for idx, b in enumerate(bids):
        bid_history.append({
            "id": str(b.id),
            "rank": idx + 1,  # อันดับ (1 = ล่าสุด/สูงสุด)
            "bidder_id": str(b.bidder.id),
            "bidder_username": b.bidder.username,
            "bidder_avatar": b.bidder.profile_image_url if hasattr(b.bidder, 'profile_image_url') else None,
            "amount": float(b.amount),
            "time": b.created_at.strftime("%H:%M:%S"),
            "date": b.created_at.strftime("%d/%m/%Y"),
            "datetime": b.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "is_highest": idx == 0  # เสนอราคาสูงสุดหรือไม่
        })
    
    # นับจำนวน unique bidders
    unique_bidders = len(set([b.bidder_id for b in bid_history]))
    
    return jsonify({
        "id": str(a.id),
        "title": a.title,
        "description": a.description,
        "image_url": a.image_url,
        "category": a.category,
        "starting_price": float(a.starting_price),
        "current_price": float(a.current_price),
        "min_bid_increment": float(a.min_bid_increment),
        "total_bids": a.total_bids,
        "unique_bidders": unique_bidders,
        "time_left": int(time_left),
        "start_time": a.start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": a.end_time.strftime("%Y-%m-%d %H:%M:%S"),
        "is_ended": a.is_ended,
        "winner": {
            "id": str(a.winner.id),
            "username": a.winner.username
        } if a.winner else None,
        "seller": {
            "id": str(a.seller.id),
            "username": a.seller.username,
            "shop_name": a.seller.shop_name
        },
        "bid_history": bid_history
    }), 200


# -----------------------------
# Place a Bid
# -----------------------------
@auction.route('/auctions/<auction_id>/bid', methods=['POST'])
@jwt_required()
def place_bid(auction_id):
    """Place a bid on an auction"""
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()
    
    if not user:
        return jsonify({"msg": "User not found"}), 404
    
    try:
        a = Auction.objects.get(id=ObjectId(auction_id))
    except:
        return jsonify({"msg": "Auction not found"}), 404
    
    # Check if auction is active
    now = datetime.utcnow()
    if a.end_time <= now or a.is_ended:
        return jsonify({"msg": "การประมูลสิ้นสุดแล้ว"}), 400
    
    if str(a.seller.id) == user_id:
        return jsonify({"msg": "ไม่สามารถประมูลสินค้าของตัวเองได้"}), 400
    
    data = request.get_json()
    bid_amount = float(data.get('amount', 0))
    
    min_bid = float(a.current_price) + float(a.min_bid_increment)
    if bid_amount < min_bid:
        return jsonify({"msg": f"ราคาต้องไม่น้อยกว่า ฿{min_bid:,.0f}"}), 400
    
    # Create bid
    new_bid = AuctionBid(
        auction=a,
        bidder=user,
        amount=bid_amount
    )
    new_bid.save()
    
    # Update auction
    a.current_price = bid_amount
    a.total_bids += 1
    a.winner = user  # Tentative winner
    a.save()
    
    # Notify previous highest bidder
    previous_bids = AuctionBid.objects(auction=a, amount__lt=bid_amount).order_by('-amount').first()
    if previous_bids and str(previous_bids.bidder.id) != user_id:
        Notification(
            user=previous_bids.bidder,
            title="⚠️ มีคนเสนอราคาสูงกว่า!",
            message=f"มีคนเสนอราคา ฿{bid_amount:,.0f} สำหรับ '{a.title}'",
            type="order",
            link=f"/auctions/{auction_id}"
        ).save()
    
    return jsonify({
        "msg": "ประมูลสำเร็จ!",
        "current_price": float(a.current_price),
        "total_bids": a.total_bids,
        "your_bid": bid_amount
    }), 200


# -----------------------------
# Create Auction (Seller)
# -----------------------------
@auction.route('/auctions', methods=['POST'])
@jwt_required()
def create_auction():
    """Create a new auction"""
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()
    
    if not user or not user.is_seller:
        return jsonify({"msg": "เฉพาะผู้ขายเท่านั้นที่สามารถสร้างการประมูลได้"}), 403
    
    data = request.get_json()
    
    title = data.get('title')
    description = data.get('description', '')
    image_url = data.get('image_url')
    category = data.get('category', 'all')
    starting_price = float(data.get('starting_price', 0))
    duration_hours = int(data.get('duration_hours', 24))  # Default 24 hours
    min_bid_increment = float(data.get('min_bid_increment', 10))
    
    if not title or starting_price <= 0:
        return jsonify({"msg": "ต้องระบุชื่อและราคาเริ่มต้น"}), 400
    
    end_time = datetime.utcnow() + timedelta(hours=duration_hours)
    
    new_auction = Auction(
        title=title,
        description=description,
        image_url=image_url,
        category=category,
        starting_price=starting_price,
        current_price=starting_price,
        min_bid_increment=min_bid_increment,
        seller=user,
        end_time=end_time
    )
    new_auction.save()
    
    return jsonify({
        "msg": "สร้างการประมูลสำเร็จ!",
        "auction_id": str(new_auction.id),
        "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S")
    }), 201


# -----------------------------
# Helper: End Auction
# -----------------------------
def end_auction(auction):
    """End an auction and notify winner"""
    auction.is_ended = True
    auction.is_active = False
    auction.save()
    
    if auction.winner:
        # Notify winner
        Notification(
            user=auction.winner,
            title="🎉 คุณชนะการประมูล!",
            message=f"คุณชนะการประมูล '{auction.title}' ในราคา ฿{float(auction.current_price):,.0f}",
            type="order",
            link=f"/auctions/{str(auction.id)}"
        ).save()
        
        # Notify seller
        Notification(
            user=auction.seller,
            title="🔨 การประมูลสิ้นสุด",
            message=f"'{auction.title}' ขายได้ในราคา ฿{float(auction.current_price):,.0f}",
            type="order",
            link=f"/auctions/{str(auction.id)}"
        ).save()


# -----------------------------
# Seed Demo Auctions
# -----------------------------
@auction.route('/auctions/seed', methods=['POST'])
def seed_auctions():
    """Create demo auctions"""
    # Get demo seller
    demo_seller = User.objects(username="P2UKAISER_Shop").first()
    if not demo_seller:
        return jsonify({"msg": "Demo seller not found"}), 404
    
    # Clear existing
    Auction.objects.delete()
    AuctionBid.objects.delete()
    
    demo_auctions = [
        {
            "title": "iPhone 15 Pro Max Limited Edition",
            "description": "iPhone 15 Pro Max สี Natural Titanium สภาพใหม่ 99% ประกันเหลือ 10 เดือน",
            "image_url": "/static/products/product_iphone_1766769641862.png",
            "category": "electronics",
            "starting_price": 25000,
            "duration_hours": 48
        },
        {
            "title": "PlayStation 5 Bundle พร้อมเกม",
            "description": "PS5 + DualSense 2 ตัว + เกม 5 แผ่น สภาพเยี่ยม",
            "image_url": "/static/products/product_ps5_1766770153698.png",
            "category": "gaming",
            "starting_price": 12000,
            "duration_hours": 24
        },
        {
            "title": "MacBook Pro M2 14 นิ้ว",
            "description": "MacBook Pro 14 M2 Pro RAM 16GB SSD 512GB ใช้งานได้ปกติ",
            "image_url": "/static/products/product_macbook_1766770139240.png",
            "category": "electronics",
            "starting_price": 35000,
            "duration_hours": 72
        },
        {
            "title": "Air Jordan 1 Retro High OG",
            "description": "รองเท้า Jordan 1 ของแท้ Size 42 สภาพ 9/10",
            "image_url": "/static/products/product_sneakers_1766769676542.png",
            "category": "fashion",
            "starting_price": 5000,
            "duration_hours": 12
        },
        {
            "title": "Apple Watch Ultra Titanium",
            "description": "Apple Watch Ultra ตัวท็อป GPS+Cellular สภาพใหม่มาก",
            "image_url": "/static/products/product_watch_1766769694809.png",
            "category": "electronics",
            "starting_price": 18000,
            "duration_hours": 36
        },
    ]
    
    created = []
    for a in demo_auctions:
        end_time = datetime.utcnow() + timedelta(hours=a['duration_hours'])
        new_auction = Auction(
            title=a['title'],
            description=a['description'],
            image_url=a['image_url'],
            category=a['category'],
            starting_price=a['starting_price'],
            current_price=a['starting_price'],
            min_bid_increment=100,
            seller=demo_seller,
            end_time=end_time
        )
        new_auction.save()
        created.append(a['title'])
    
    return jsonify({
        "msg": f"Created {len(created)} demo auctions",
        "auctions": created
    }), 201


# -----------------------------
# Auto-Bid: Set Auto Bid
# -----------------------------
@auction.route('/auctions/<auction_id>/auto-bid', methods=['POST'])
@jwt_required()
def set_auto_bid(auction_id):
    """Set auto-bid for an auction"""
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()
    
    if not user:
        return jsonify({"msg": "User not found"}), 404
    
    try:
        a = Auction.objects.get(id=ObjectId(auction_id))
    except:
        return jsonify({"msg": "Auction not found"}), 404
    
    if a.is_ended or datetime.utcnow() >= a.end_time:
        return jsonify({"msg": "การประมูลสิ้นสุดแล้ว"}), 400
    
    if str(a.seller.id) == user_id:
        return jsonify({"msg": "ไม่สามารถประมูลสินค้าของตัวเองได้"}), 400
    
    data = request.get_json()
    max_amount = float(data.get('max_amount', 0))
    
    min_bid = float(a.current_price) + float(a.min_bid_increment)
    if max_amount < min_bid:
        return jsonify({"msg": f"ราคาสูงสุดต้องไม่น้อยกว่า ฿{min_bid:,.0f}"}), 400
    
    # Check existing auto-bid
    existing = AutoBid.objects(auction=a, user=user, is_active=True).first()
    if existing:
        existing.max_amount = max_amount
        existing.save()
        msg = "อัปเดต Auto-Bid สำเร็จ"
    else:
        AutoBid(
            auction=a,
            user=user,
            max_amount=max_amount
        ).save()
        msg = "ตั้งค่า Auto-Bid สำเร็จ"
    
    # Process auto-bid immediately
    process_auto_bids(a)
    
    return jsonify({
        "msg": msg,
        "max_amount": max_amount,
        "current_price": float(a.current_price)
    }), 200


# -----------------------------
# Auto-Bid: Cancel Auto Bid
# -----------------------------
@auction.route('/auctions/<auction_id>/auto-bid', methods=['DELETE'])
@jwt_required()
def cancel_auto_bid(auction_id):
    """Cancel auto-bid for an auction"""
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()
    
    try:
        a = Auction.objects.get(id=ObjectId(auction_id))
    except:
        return jsonify({"msg": "Auction not found"}), 404
    
    auto_bid = AutoBid.objects(auction=a, user=user, is_active=True).first()
    if not auto_bid:
        return jsonify({"msg": "ไม่พบ Auto-Bid"}), 404
    
    auto_bid.is_active = False
    auto_bid.save()
    
    return jsonify({"msg": "ยกเลิก Auto-Bid สำเร็จ"}), 200


# -----------------------------
# Auto-Bid: Get My Auto Bids
# -----------------------------
@auction.route('/auctions/my-auto-bids', methods=['GET'])
@jwt_required()
def get_my_auto_bids():
    """Get all active auto-bids for current user"""
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()
    
    auto_bids = AutoBid.objects(user=user, is_active=True)
    
    result = []
    for ab in auto_bids:
        a = ab.auction
        if a.is_ended:
            continue
        
        result.append({
            "id": str(ab.id),
            "auction_id": str(a.id),
            "auction_title": a.title,
            "auction_image": a.image_url,
            "max_amount": float(ab.max_amount),
            "current_bid": float(ab.current_bid),
            "current_price": float(a.current_price),
            "is_winning": str(a.winner.id) == user_id if a.winner else False,
            "time_left": max(0, int((a.end_time - datetime.utcnow()).total_seconds()))
        })
    
    return jsonify({"auto_bids": result}), 200


# -----------------------------
# Get Seller's Auctions
# -----------------------------
@auction.route('/auctions/my-auctions', methods=['GET'])
@jwt_required()
def get_my_auctions():
    """Get all auctions created by the current seller"""
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()
    
    if not user:
        return jsonify({"msg": "User not found"}), 404
    
    if not user.is_seller:
        return jsonify({"msg": "เฉพาะผู้ขายเท่านั้น"}), 403
    
    now = datetime.utcnow()
    
    # Get all auctions by this seller
    seller_auctions = Auction.objects(seller=user).order_by('-created_at')
    
    active = []
    ended = []
    
    for a in seller_auctions:
        time_left = (a.end_time - now).total_seconds() if a.end_time > now else 0
        
        auction_data = {
            "id": str(a.id),
            "title": a.title,
            "description": a.description,
            "image_url": a.image_url,
            "category": a.category,
            "starting_price": float(a.starting_price),
            "current_price": float(a.current_price),
            "total_bids": a.total_bids,
            "time_left": int(time_left),
            "end_time": a.end_time.strftime("%Y-%m-%d %H:%M:%S"),
            "is_ended": a.is_ended,
            "winner": {
                "id": str(a.winner.id),
                "username": a.winner.username
            } if a.winner else None
        }
        
        if a.is_ended or a.end_time <= now:
            ended.append(auction_data)
        else:
            active.append(auction_data)
    
    return jsonify({
        "active": active,
        "ended": ended,
        "stats": {
            "total": len(seller_auctions),
            "active": len(active),
            "ended": len(ended)
        }
    }), 200


# -----------------------------
# Auction History
# -----------------------------
@auction.route('/auctions/my-history', methods=['GET'])
@jwt_required()
def get_my_auction_history():
    """Get user's auction participation history"""
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()
    
    # Get unique auctions user has bid on
    user_bids = AuctionBid.objects(bidder=user).order_by('-created_at')
    auction_ids = list(set([str(b.auction.id) for b in user_bids]))
    
    result = {
        "won": [],
        "lost": [],
        "active": []
    }
    
    for aid in auction_ids:
        try:
            a = Auction.objects.get(id=ObjectId(aid))
        except:
            continue
        
        # Get user's highest bid
        user_highest = AuctionBid.objects(auction=a, bidder=user).order_by('-amount').first()
        
        auction_data = {
            "id": str(a.id),
            "title": a.title,
            "image_url": a.image_url,
            "current_price": float(a.current_price),
            "my_highest_bid": float(user_highest.amount) if user_highest else 0,
            "total_bids": a.total_bids,
            "end_time": a.end_time.isoformat(),
            "is_ended": a.is_ended
        }
        
        if a.is_ended:
            if a.winner and str(a.winner.id) == user_id:
                result["won"].append(auction_data)
            else:
                result["lost"].append(auction_data)
        else:
            auction_data["time_left"] = max(0, int((a.end_time - datetime.utcnow()).total_seconds()))
            auction_data["is_winning"] = str(a.winner.id) == user_id if a.winner else False
            result["active"].append(auction_data)
    
    return jsonify({
        "history": result,
        "stats": {
            "total_participated": len(auction_ids),
            "won": len(result["won"]),
            "lost": len(result["lost"]),
            "active": len(result["active"])
        }
    }), 200


# -----------------------------
# Helper: Process Auto-Bids
# -----------------------------
def process_auto_bids(auction):
    """Process all auto-bids for an auction"""
    if auction.is_ended:
        return
    
    # Get all active auto-bids, sorted by max_amount (highest first)
    auto_bids = AutoBid.objects(auction=auction, is_active=True).order_by('-max_amount')
    
    if len(auto_bids) < 1:
        return
    
    current_price = float(auction.current_price)
    increment = float(auction.min_bid_increment)
    
    # If only one auto-bidder, bid minimum
    if len(auto_bids) == 1:
        ab = auto_bids[0]
        if float(ab.max_amount) > current_price:
            new_price = current_price + increment
            if new_price <= float(ab.max_amount):
                place_auto_bid(auction, ab.user, new_price)
                ab.current_bid = new_price
                ab.save()
        return
    
    # Multiple auto-bidders: compete
    highest = auto_bids[0]
    second = auto_bids[1]
    
    # New price beats second highest by one increment
    new_price = min(float(highest.max_amount), float(second.max_amount) + increment)
    
    if new_price > current_price:
        place_auto_bid(auction, highest.user, new_price)
        highest.current_bid = new_price
        highest.save()


def place_auto_bid(auction, user, amount):
    """Place an auto-bid"""
    new_bid = AuctionBid(
        auction=auction,
        bidder=user,
        amount=amount
    )
    new_bid.save()
    
    # Update auction
    old_winner = auction.winner
    auction.current_price = amount
    auction.total_bids += 1
    auction.winner = user
    auction.save()
    
    # Notify previous winner if different
    if old_winner and str(old_winner.id) != str(user.id):
        Notification(
            user=old_winner,
            title="⚠️ Auto-Bid: มีคนเสนอราคาสูงกว่า!",
            message=f"มีคนเสนอราคา ฿{amount:,.0f} สำหรับ '{auction.title}'",
            type="order",
            link=f"/auctions/{str(auction.id)}"
        ).save()

