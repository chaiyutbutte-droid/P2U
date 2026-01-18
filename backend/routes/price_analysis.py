from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from datetime import datetime
import statistics

from models import Product, PriceStatistics

price_analysis = Blueprint('price_analysis', __name__)


# ========= Helper: Calculate Price Statistics =========
def calculate_category_stats(category):
    """Calculate price statistics for a category"""
    if category == 'all':
        products = Product.objects()
    else:
        products = Product.objects(category=category)
    
    if not products:
        return None
    
    prices = [float(p.price) for p in products]
    
    if not prices:
        return None
    
    return {
        'category': category,
        'avg_price': round(statistics.mean(prices), 2),
        'min_price': round(min(prices), 2),
        'max_price': round(max(prices), 2),
        'median_price': round(statistics.median(prices), 2),
        'total_products': len(prices),
        'std_dev': round(statistics.stdev(prices), 2) if len(prices) > 1 else 0
    }


def get_price_distribution(prices):
    """Get price distribution buckets"""
    if not prices:
        return {}
    
    max_price = max(prices)
    
    # Define buckets based on percentiles
    buckets = {
        'budget': {'range': [0, max_price * 0.3], 'count': 0},
        'mid': {'range': [max_price * 0.3, max_price * 0.7], 'count': 0},
        'premium': {'range': [max_price * 0.7, max_price], 'count': 0}
    }
    
    for price in prices:
        if price <= max_price * 0.3:
            buckets['budget']['count'] += 1
        elif price <= max_price * 0.7:
            buckets['mid']['count'] += 1
        else:
            buckets['premium']['count'] += 1
    
    # Round range values
    for bucket in buckets.values():
        bucket['range'] = [round(bucket['range'][0], 2), round(bucket['range'][1], 2)]
    
    return buckets


# ========= Get Price Stats by Category =========
@price_analysis.route('/price/category/<category>', methods=['GET'])
def get_price_by_category(category):
    """Get price statistics for a specific category"""
    stats = calculate_category_stats(category)
    
    if not stats:
        return jsonify({
            'msg': 'ไม่พบสินค้าในหมวดหมู่นี้',
            'category': category,
            'total_products': 0
        }), 404
    
    # Get price distribution
    if category == 'all':
        products = Product.objects()
    else:
        products = Product.objects(category=category)
    
    prices = [float(p.price) for p in products]
    stats['price_distribution'] = get_price_distribution(prices)
    
    return jsonify(stats), 200


# ========= Get Similar Product Prices =========
@price_analysis.route('/price/similar/<product_id>', methods=['GET'])
def get_similar_prices(product_id):
    """Get prices of similar products (same category)"""
    try:
        product = Product.objects(id=ObjectId(product_id)).first()
        if not product:
            return jsonify({'msg': 'ไม่พบสินค้า'}), 404
        
        # Get products in same category
        similar_products = Product.objects(
            category=product.category,
            id__ne=ObjectId(product_id)
        ).limit(20)
        
        similar_data = [{
            'id': str(p.id),
            'name': p.name,
            'price': float(p.price),
            'image_url': p.image_url,
            'seller': p.seller.shop_name if p.seller and p.seller.shop_name else p.seller.username if p.seller else 'Unknown'
        } for p in similar_products]
        
        # Calculate price comparison
        prices = [float(p.price) for p in similar_products]
        current_price = float(product.price)
        
        comparison = {
            'current_price': current_price,
            'position': 'average'
        }
        
        if prices:
            avg = statistics.mean(prices)
            if current_price < avg * 0.8:
                comparison['position'] = 'below_average'
                comparison['label'] = '🟢 ราคาดี'
            elif current_price > avg * 1.2:
                comparison['position'] = 'above_average'
                comparison['label'] = '🔴 ราคาสูง'
            else:
                comparison['position'] = 'average'
                comparison['label'] = '🟡 ราคาปกติ'
            
            comparison['avg_market_price'] = round(avg, 2)
            comparison['difference_percent'] = round(((current_price - avg) / avg) * 100, 1)
        
        return jsonify({
            'product': {
                'id': str(product.id),
                'name': product.name,
                'price': current_price,
                'category': product.category
            },
            'similar_products': similar_data,
            'comparison': comparison
        }), 200
        
    except Exception as e:
        return jsonify({'msg': str(e)}), 500


# ========= Get Price Recommendation =========
@price_analysis.route('/price/recommendation', methods=['POST'])
def get_price_recommendation():
    """Get recommended price range for a new product"""
    data = request.get_json()
    category = data.get('category', 'all')
    name = data.get('name', '')
    
    # Get category stats
    stats = calculate_category_stats(category)
    
    if not stats:
        # Return default recommendation if no data
        return jsonify({
            'category': category,
            'has_data': False,
            'recommendation': {
                'competitive_price': 0,
                'average_price': 0,
                'premium_price': 0,
                'suggested_range': [0, 0]
            },
            'msg': 'ไม่มีข้อมูลราคาในหมวดหมู่นี้'
        }), 200
    
    avg = stats['avg_price']
    median = stats['median_price']
    
    recommendation = {
        'competitive_price': round(avg * 0.85, 2),  # 15% below average
        'average_price': round(avg, 2),
        'premium_price': round(avg * 1.3, 2),  # 30% above average
        'suggested_range': [round(avg * 0.7, 2), round(avg * 1.5, 2)],
        'median_price': median
    }
    
    return jsonify({
        'category': category,
        'has_data': True,
        'stats': stats,
        'recommendation': recommendation,
        'tips': [
            f'💡 ราคาเฉลี่ยในหมวดหมู่นี้คือ ฿{avg:,.0f}',
            f'📊 มีสินค้า {stats["total_products"]} รายการในหมวดหมู่นี้',
            '🏆 ราคาแข่งขันได้ควรอยู่ระหว่าง ฿{:,.0f} - ฿{:,.0f}'.format(
                recommendation['competitive_price'],
                recommendation['average_price']
            )
        ]
    }), 200


# ========= Get All Categories Stats =========
@price_analysis.route('/price/all-categories', methods=['GET'])
def get_all_categories_stats():
    """Get price statistics for all categories"""
    categories = ['all', 'electronics', 'fashion', 'gaming', 'beauty', 'home', 'sports']
    
    all_stats = []
    for cat in categories:
        stats = calculate_category_stats(cat)
        if stats:
            all_stats.append(stats)
    
    return jsonify({
        'categories': all_stats,
        'updated_at': datetime.utcnow().isoformat()
    }), 200


# ========= Update Price Statistics Cache =========
@price_analysis.route('/price/update-stats', methods=['POST'])
def update_price_statistics():
    """Update cached price statistics (admin only)"""
    categories = ['all', 'electronics', 'fashion', 'gaming', 'beauty', 'home', 'sports']
    
    updated = []
    for cat in categories:
        stats = calculate_category_stats(cat)
        if stats:
            # Upsert to PriceStatistics collection
            price_stat = PriceStatistics.objects(category=cat).first()
            if not price_stat:
                price_stat = PriceStatistics(category=cat)
            
            price_stat.avg_price = stats['avg_price']
            price_stat.min_price = stats['min_price']
            price_stat.max_price = stats['max_price']
            price_stat.median_price = stats['median_price']
            price_stat.total_products = stats['total_products']
            price_stat.updated_at = datetime.utcnow()
            price_stat.save()
            
            updated.append(cat)
    
    return jsonify({
        'msg': 'อัปเดตสถิติราคาเรียบร้อย',
        'updated_categories': updated
    }), 200
