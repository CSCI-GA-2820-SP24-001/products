######################################################################
# Copyright 2016, 2024 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

"""
Product Store Service

This service implements a REST API that allows you to Create, Read, Update
and Delete Products from the inventory of products in the ProductShop
"""

from flask import jsonify, request, url_for, abort
from flask import current_app as app  # Import Flask application
from service.models import Product
from service.common import status  # HTTP Status Codes


######################################################################
# GET INDEX
######################################################################
# @app.route("/")
# def index():
#     """Root URL response"""
#     return (
#         "Welcome to the Products Team! Try adding /products to the end of this URL to explore.",
#         status.HTTP_200_OK,
#     )


@app.route("/")
def index():
    """Base URL for our service"""
    return app.send_static_file("index.html")


######################################################################
# GET HEALTH CHECK
######################################################################
@app.route("/health")
def health_check():
    """Let them know our heart is still beating"""
    return jsonify(status=200, message="Healthy"), status.HTTP_200_OK


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################


######################################################################
# CREATE A NEW PRODUCT
######################################################################
@app.route("/products", methods=["POST"])
def create_products():
    """
    Creates a Product

    This endpoint will create a Product based the data in the body that is posted
    """
    app.logger.info("Request to create a product")
    check_content_type("application/json")

    product = Product()
    product.deserialize(request.get_json())
    product.create()
    message = product.serialize()
    location_url = url_for("get_products", product_id=product.id, _external=True)
    # location_url = "unknown"

    app.logger.info("Product with ID: %d created.", product.id)
    return jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}


######################################################################
# READ A PRODUCT
######################################################################
@app.route("/products/<int:product_id>", methods=["GET"])
def get_products(product_id):
    """
    Retrieve a single Product

    This endpoint will return a Product based on it's id
    """
    app.logger.info("Request for product with id: %s", product_id)

    product = Product.find(product_id)
    if not product:
        error(
            status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found."
        )

    app.logger.info("Returning product: %s", product.name)
    return jsonify(product.serialize()), status.HTTP_200_OK


######################################################################
# LIST ALL PRODUCTS
######################################################################
@app.route("/products", methods=["GET"])
def list_products():
    """Returns all of the Products"""
    app.logger.info("Request for product list")

    products = []

    # See if any query filters were passed in
    category = request.args.get("category")
    name = request.args.get("name")
    if category:
        products = Product.find_by_category(category)
    elif name:
        products = Product.find_by_name(name)
    else:
        products = Product.all()

    results = [product.serialize() for product in products]
    app.logger.info("Returning %d products", len(results))
    return jsonify(results), status.HTTP_200_OK


######################################################################
# UPDATE AN EXISTING PRODUCT
######################################################################
@app.route("/products/<int:product_id>", methods=["PUT"])
def update_products(product_id):
    """
    Update a Product

    This endpoint will update a Product based the body that is posted
    """
    app.logger.info("Request to update product with id: %d", product_id)
    check_content_type("application/json")

    product = Product.find(product_id)
    if not product:
        error(
            status.HTTP_404_NOT_FOUND, f"Product with id: '{product_id}' was not found."
        )

    product.deserialize(request.get_json())
    product.id = product_id
    product.update()

    app.logger.info("Product with ID: %d updated.", product.id)
    return jsonify(product.serialize()), status.HTTP_200_OK


######################################################################
# DELETE A PRODUCT
######################################################################
@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_products(product_id):
    """
    Delete a Product

    This endpoint will delete a Product based the id specified in the path
    """
    app.logger.info("Request to delete product with id: %d", product_id)

    product = Product.find(product_id)
    if product:
        product.delete()

    app.logger.info("Product with ID: %d delete complete.", product_id)
    return "", status.HTTP_204_NO_CONTENT


######################################################################
# LIKE A PRODUCT
######################################################################
@app.route("/products/like/<int:product_id>", methods=["PUT"])
def like_products(product_id):
    """
    Like an existing Product
    This endpoint will update total likes of a Product
    """
    app.logger.info("Request to like product with id: %s", product_id)
    check_content_type("application/json")

    product = Product.find(product_id)
    if not product:
        abort(
            status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found."
        )

    product.like += 1
    product.id = product_id
    product.update()
    message = product.serialize()

    app.logger.info("Product with id [%s] liked.", product.id)
    return jsonify(message), status.HTTP_200_OK


######################################################################
# Checks the ContentType of a request
######################################################################
def check_content_type(content_type):
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        error(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )

    if request.headers["Content-Type"] == content_type:
        return

    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    error(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )


######################################################################
# Logs error messages before aborting
######################################################################
def error(status_code, reason):
    """Logs the error and then aborts"""
    app.logger.error(reason)
    abort(status_code, reason)
