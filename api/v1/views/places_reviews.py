#!/usr/bin/python3
""" Api for Review """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews/', methods=['GET'],
                 strict_slashes=False)
def get_all_reviews(place_id):
    """ get all review by place id  """
    json_list = []

    place = storage.get(Place, palce_id)
    if place is None:
        abort(404)

    places = place.reviews
    for place_r in places:
        json_list.append(place_r.to_dict())
    return jsonify(json_list)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    '''Retrieves a review for a place'''
    reviews = storage.get('Review', review_id)
    if reviews is None:
        abort(404)
    return jsonify(reviews.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_reviews(review_id):
    ''' Deletes a review object from storage '''
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)

        review.delete()
        storage.save()

        return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    '''Creates an instance of Review and save it to storage'''
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    form = request.get_json()
    if form is None:
        abort(404, "Not a JSON")

    if "user_id" not in form:
        abort(400, "Missing user_id")

    user = storage.get(User, form.get("user_id"))
    if user is None:
        abort(404)

    if "text" not in form:
        abort(400, "Missing text")

    form['place_id'] = place_id
    new_place = Review(**form)
    storage.new(new_place)
    storage.save()

    return (jsonify(new_place.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    '''Updates Review object attribute'''
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    form = request.get_json(force=True)
    if form is None:
        abort(400, "Not a JSON")

    for key, value in form.items():
        if key not in ["id", "user_id", "place_id", "created_at",
                       "updated_at"]:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict())
