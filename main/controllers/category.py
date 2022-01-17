from flask import jsonify

from main import app, db
from main.commons.decorators import check_category_exist, validate_input, validate_token
from main.commons.exceptions import CategoryDeleteForbidden, CategoryExisted
from main.models.category import Category
from main.schemas import CategorySchema, PageSchema


@app.get("/categories")
@validate_input(PageSchema)
def get_categories(page, **__):
    paginated_categories = Category.query.paginate(
        page=page, per_page=app.config["PER_PAGE"]
    )
    categories = CategorySchema(many=True).dump(paginated_categories.items)

    return jsonify(
        {
            "items": categories,
            "items_per_page": paginated_categories.per_page,
            "total": paginated_categories.total,
        }
    )


@app.post("/categories")
@validate_token
@validate_input(CategorySchema)
def create_category(user_id, name, **__):
    existing_category = Category.query.filter_by(name=name).one_or_none()
    if existing_category:
        raise CategoryExisted()

    new_category = Category(name=name, user_id=user_id)
    db.session.add(new_category)
    db.session.commit()

    return CategorySchema().jsonify(new_category, many=False)


@app.delete("/categories/<int:category_id>")
@validate_token
@check_category_exist
def delete_category(*_, category, user_id, **__):
    # if request user is not the owner of this category
    if category.user_id != user_id:
        raise CategoryDeleteForbidden()

    db.session.delete(category)
    db.session.commit()

    return jsonify({})
