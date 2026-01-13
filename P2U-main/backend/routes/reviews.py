from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from mongoengine.errors import DoesNotExist, ValidationError

from models import User, Product, Review, Notification

reviews = Blueprint('reviews', __name__)


# -----------------------------
# Create a Review
# -----------------------------
@reviews.route('/reviews', methods=['POST'])
@jwt_required()
def create_review():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    product_id = data.get('product_id')
    rating = data.get('rating')
    comment = data.get('comment', '')
    
    if not product_id or not rating:
        return jsonify({"msg": "Product ID and rating are required"}), 400
    
    if not (1 <= int(rating) <= 5):
        return jsonify({"msg": "Rating must be between 1 and 5"}), 400
    
    try:
        user = User.objects.get(id=ObjectId(user_id))
        product = Product.objects.get(id=ObjectId(product_id))
        
        # Check if user already reviewed this product
        existing_review = Review.objects(user=user, product=product).first()
        if existing_review:
            return jsonify({"msg": "You have already reviewed this product"}), 400
        
        review = Review(
            product=product,
            user=user,
            rating=int(rating),
            comment=comment
        )
        review.save()
        
        # Create notification for seller
        Notification(
            user=product.seller,
            title="New Review",
            message=f"{user.username} reviewed your product '{product.name}'",
            type="review",
            link=f"/product/{product_id}"
        ).save()
        
        # Update seller's average rating
        all_reviews = Review.objects(product__in=Product.objects(seller=product.seller))
        if all_reviews:
            avg_rating = sum(r.rating for r in all_reviews) / len(all_reviews)
            product.seller.rating_avg = avg_rating
            product.seller.save()
        
        return jsonify({
            "msg": "Review created successfully",
            "review": {
                "id": str(review.id),
                "rating": review.rating,
                "comment": review.comment,
                "user": user.username,
                "created_at": review.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }
        }), 201
        
    except DoesNotExist:
        return jsonify({"msg": "Product not found"}), 404
    except Exception as e:
        return jsonify({"msg": str(e)}), 500


# -----------------------------
# Get Reviews for a Product
# -----------------------------
@reviews.route('/reviews/product/<product_id>', methods=['GET'])
def get_product_reviews(product_id):
    try:
        product = Product.objects.get(id=ObjectId(product_id))
        reviews_list = Review.objects(product=product).order_by('-created_at')
        
        result = []
        total_rating = 0
        for r in reviews_list:
            total_rating += r.rating
            result.append({
                "id": str(r.id),
                "rating": r.rating,
                "comment": r.comment,
                "user": {
                    "id": str(r.user.id),
                    "username": r.user.username,
                    "profile_image_url": r.user.profile_image_url
                },
                "created_at": r.created_at.strftime("%Y-%m-%d %H:%M:%S")
            })
        
        avg_rating = total_rating / len(reviews_list) if reviews_list else 0
        
        return jsonify({
            "reviews": result,
            "total": len(result),
            "average_rating": round(avg_rating, 1)
        }), 200
        
    except DoesNotExist:
        return jsonify({"msg": "Product not found"}), 404


# -----------------------------
# Get Reviews for a Seller
# -----------------------------
@reviews.route('/reviews/seller/<seller_id>', methods=['GET'])
def get_seller_reviews(seller_id):
    try:
        seller = User.objects.get(id=ObjectId(seller_id))
        products = Product.objects(seller=seller)
        reviews_list = Review.objects(product__in=products).order_by('-created_at')
        
        result = []
        total_rating = 0
        for r in reviews_list:
            total_rating += r.rating
            result.append({
                "id": str(r.id),
                "rating": r.rating,
                "comment": r.comment,
                "product": {
                    "id": str(r.product.id),
                    "name": r.product.name
                },
                "user": {
                    "id": str(r.user.id),
                    "username": r.user.username
                },
                "created_at": r.created_at.strftime("%Y-%m-%d %H:%M:%S")
            })
        
        avg_rating = total_rating / len(reviews_list) if reviews_list else 0
        
        return jsonify({
            "reviews": result,
            "total": len(result),
            "average_rating": round(avg_rating, 1)
        }), 200
        
    except DoesNotExist:
        return jsonify({"msg": "Seller not found"}), 404


# -----------------------------
# Delete Review (owner only)
# -----------------------------
@reviews.route('/reviews/<review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    user_id = get_jwt_identity()
    
    try:
        review = Review.objects.get(id=ObjectId(review_id))
        
        if str(review.user.id) != user_id:
            return jsonify({"msg": "Unauthorized"}), 403
        
        review.delete()
        return jsonify({"msg": "Review deleted successfully"}), 200
        
    except DoesNotExist:
        return jsonify({"msg": "Review not found"}), 404
