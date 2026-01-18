from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from collections import Counter

from models import User, Product, Order, Review

recommendations = Blueprint('recommendations', __name__)


# -----------------------------
# "Also Bought" Recommendations
# -----------------------------
@recommendations.route('/recommendations/also-bought/<product_id>', methods=['GET'])
def get_also_bought(product_id):
    """Get products that users also bought with this product"""
    try:
        target_product = Product.objects.get(id=ObjectId(product_id))
    except:
        return jsonify({"msg": "Product not found"}), 404
    
    # Find orders containing this product
    orders_with_product = Order.objects(items__product_id=product_id)
    
    # Collect other products from those orders
    related_product_ids = Counter()
    for order in orders_with_product:
        for item in order.items:
            if item.get('product_id') != product_id:
                related_product_ids[item.get('product_id')] += 1
    
    # Get top 6 related products
    top_product_ids = [pid for pid, _ in related_product_ids.most_common(6)]
    
    products = []
    for pid in top_product_ids:
        try:
            product = Product.objects.get(id=ObjectId(pid))
            products.append({
                "id": str(product.id),
                "name": product.name,
                "price": float(product.price),
                "image_url": product.image_url,
                "seller": {
                    "id": str(product.seller.id),
                    "username": product.seller.username,
                    "shop_name": product.seller.shop_name
                } if product.seller else None
            })
        except:
            continue
    
    return jsonify({"products": products}), 200


# -----------------------------
# Daily Recommendations
# -----------------------------
@recommendations.route('/recommendations/daily', methods=['GET'])
def get_daily_recommendations():
    """Get random popular products for the day"""
    # Get random products (simple approach: latest products with good reviews)
    products = Product.objects.order_by('-created_at').limit(12)
    
    result = []
    for product in products:
        # Get average rating
        reviews = Review.objects(product=product)
        avg_rating = 0
        if reviews:
            avg_rating = sum(r.rating for r in reviews) / len(reviews)
        
        result.append({
            "id": str(product.id),
            "name": product.name,
            "price": float(product.price),
            "image_url": product.image_url,
            "rating": round(avg_rating, 1),
            "review_count": len(reviews),
            "seller": {
                "id": str(product.seller.id),
                "username": product.seller.username,
                "shop_name": product.seller.shop_name
            } if product.seller else None
        })
    
    return jsonify({"products": result}), 200


# -----------------------------
# Personalized "For You"
# -----------------------------
@recommendations.route('/recommendations/for-you', methods=['GET'])
@jwt_required()
def get_for_you():
    """Get personalized recommendations based on user's wishlist and purchase history"""
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()
    
    if not user:
        return jsonify({"msg": "User not found"}), 404
    
    # Get user's purchased products
    user_orders = Order.objects(user=user)
    purchased_ids = set()
    purchased_sellers = set()
    
    for order in user_orders:
        for item in order.items:
            purchased_ids.add(item.get('product_id'))
            # Track sellers user bought from
    
    # Get wishlist product categories/sellers
    wishlist_sellers = set()
    for product in user.wishlist:
        if product and product.seller:
            wishlist_sellers.add(str(product.seller.id))
    
    # Recommend products from same sellers or similar price range
    preferred_sellers = purchased_sellers.union(wishlist_sellers)
    
    recommended = []
    
    # Get products from preferred sellers
    if preferred_sellers:
        for seller_id in list(preferred_sellers)[:3]:
            try:
                products = Product.objects(seller=ObjectId(seller_id)).limit(4)
                for p in products:
                    if str(p.id) not in purchased_ids:
                        recommended.append(p)
            except:
                continue
    
    # Fill with popular products if not enough
    if len(recommended) < 8:
        popular = Product.objects.order_by('-created_at').limit(12)
        for p in popular:
            if str(p.id) not in purchased_ids and p not in recommended:
                recommended.append(p)
                if len(recommended) >= 12:
                    break
    
    result = []
    for product in recommended[:12]:
        reviews = Review.objects(product=product)
        avg_rating = sum(r.rating for r in reviews) / len(reviews) if reviews else 0
        
        result.append({
            "id": str(product.id),
            "name": product.name,
            "price": float(product.price),
            "image_url": product.image_url,
            "rating": round(avg_rating, 1),
            "seller": {
                "id": str(product.seller.id),
                "username": product.seller.username,
                "shop_name": product.seller.shop_name
            } if product.seller else None
        })
    
    return jsonify({"products": result}), 200


# -----------------------------
# Similar Products
# -----------------------------
@recommendations.route('/recommendations/similar/<product_id>', methods=['GET'])
def get_similar_products(product_id):
    """Get products with similar price range from same seller"""
    try:
        target = Product.objects.get(id=ObjectId(product_id))
    except:
        return jsonify({"msg": "Product not found"}), 404
    
    price = float(target.price)
    min_price = price * 0.5
    max_price = price * 1.5
    
    # Get products from same seller in similar price range
    similar = Product.objects(
        id__ne=target.id,
        price__gte=min_price,
        price__lte=max_price
    ).limit(6)
    
    result = []
    for product in similar:
        result.append({
            "id": str(product.id),
            "name": product.name,
            "price": float(product.price),
            "image_url": product.image_url,
            "seller": {
                "id": str(product.seller.id),
                "username": product.seller.username,
                "shop_name": product.seller.shop_name
            } if product.seller else None
        })
    
    return jsonify({"products": result}), 200
