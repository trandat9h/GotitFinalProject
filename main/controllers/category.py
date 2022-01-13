from flask import jsonify, request

from main import app, db
from main.commons.exceptions import BadRequest, Forbidden, InternalServerError
from main.engines import check_category_exist
from main.libs import validate_input, validate_token
from main.models.category import Category
from main.schemas import CategorySchema


@app.get("/categories")
@validate_token
def get_categories(*_, **__):
    try:
        page = int(request.args.get("page"))
    except KeyError:
        # this handler is not yet listed in design docs
        # Key error is not running when
        raise BadRequest(error_code=400010, error_message="page is not provided")

    try:
        paginated_categories = Category.query.paginate(page=page, per_page=2)
        categories = CategorySchema(many=True).dump(paginated_categories.items)
    except Exception as e:
        raise InternalServerError(error_message=str(e))

    return (
        jsonify(
            {
                "items": categories,
                "items_per_page": len(categories),
                "total": paginated_categories.total,
            }
        ),
        200,
    )


@app.post("/categories")
@validate_token
@validate_input(CategorySchema)
def create_category(*_, user_id, name, **__):
    try:
        existed_category = Category.query.filter_by(name=name).one_or_none()
    except Exception as e:
        raise InternalServerError(error_message=str(e))
    if existed_category:
        raise BadRequest(
            error_message=f"Category {name}already existed.", error_code=400005
        )

    try:
        new_category = Category(name=name, user_id=user_id)
        db.session.add(new_category)
        db.session.commit()
    except Exception as e:
        raise InternalServerError(error_message=str(e))

    return jsonify({}), 200


@app.delete("/categories/<int:category_id>")
@validate_token
@check_category_exist
def delete_category(*_, category, user_id, **__):
    if category.user_id != user_id:
        raise Forbidden(
            error_message="This user is not allowed to delete this category.",
            error_code=403001,
        )
    try:
        db.session.delete(category)
        db.session.commit()
    except Exception as e:
        raise InternalServerError(error_message=str(e))
    return jsonify({}), 200
