from flask import jsonify, request

from main import app, db
from main.commons.exceptions import BadRequest, Forbidden, InternalServerError
from main.engines import check_category_exist, check_item_exist
from main.libs import validate_input, validate_token
from main.models.item import Item
from main.schemas import ItemSchema


@app.get("/categories/<int:category_id>/items")
@validate_token
@check_category_exist
def get_items(*_, category, **__):
    try:
        page = int(request.args.get("page"))
        print(type(page))
    except KeyError:
        # this handler is not yet listed in design docs
        raise BadRequest(error_code=400010, error_message="page is not provided")

    paginated_items = category.items.paginate(page=page, per_page=3)
    items = ItemSchema(many=True).dump(paginated_items.items)
    # any pagination method to count items length besides list len?
    return (
        jsonify(
            {
                "items": items,
                "items_per_page": len(items),
                "total_items": paginated_items.total,
            }
        ),
        200,
    )


@app.post("/categories/<int:category_id>/items")
@validate_token
@validate_input(ItemSchema)
@check_category_exist
def create_item(*_, category, user_id, name, description, **__):
    try:
        existed_item = Item.query.filter_by(name=name).one_or_none()
    except Exception as e:
        raise InternalServerError(error_message=str(e))

    if existed_item:
        raise BadRequest(
            error_message=f"item {name} already existed.", error_code=400003
        )

    try:
        new_item = Item(
            name=name, description=description, category_id=category.id, user_id=user_id
        )
        db.session.add(new_item)
        db.session.commit()
    except Exception as e:
        raise InternalServerError(error_message=str(e))
    return jsonify({}), 200


@app.get("/categories/<int:category_id>/items/<int:item_id>")
@validate_token
@check_category_exist
@check_item_exist
def get_item(*_, item, **__):
    return jsonify(ItemSchema().dump(item)), 200


@app.put("/categories/<int:category_id>/items/<int:item_id>")
@validate_token
@validate_input(ItemSchema)
@check_category_exist
@check_item_exist
def update_item(*_, name, description, item, user_id, **__):
    if item.user_id != user_id:
        raise Forbidden(
            error_message="This user is not allowed to update this item.",
            error_code=403002,
        )

    # check for existed item name
    try:
        existed_item = Item.query.filter_by(name=name).one_or_none()
    except Exception as e:
        raise InternalServerError(error_message=str(e))

    # if another item with input name existed
    if existed_item and existed_item.id != item.id:
        raise BadRequest(
            error_message=f"Item {name} is already existed.", error_code=400003
        )

    try:
        item.name = name
        item.description = description
        db.session.commit()
    except Exception as e:
        raise InternalServerError(error_message=str(e))

    return jsonify({}), 200


@app.delete("/categories/<int:category_id>/items/<int:item_id>")
@validate_token
@check_category_exist
@check_item_exist
def delete_item(*_, item, user_id, **__):
    if item.user_id != user_id:
        raise Forbidden(
            error_message="This user is not allowed to update this item.",
            error_code=403002,
        )

    try:
        db.session.delete(item)
        db.session.commit()
    except Exception as e:
        raise InternalServerError(error_message=str(e))

    return jsonify({}), 200
