from flask import jsonify

from main import app, db
from main.commons.decorators import (
    check_category_exist,
    check_item_exist,
    validate_input,
    validate_token,
)
from main.commons.exceptions import (
    ItemDeleteForbidden,
    ItemExisted,
    ItemUpdateForbidden,
)
from main.models.item import Item
from main.schemas import ItemSchema, PageSchema


@app.get("/categories/<int:category_id>/items")
@validate_input(PageSchema)
@check_category_exist
def get_items(category, page, **__):
    paginated_items = category.items.paginate(
        page=page, per_page=app.config["PER_PAGE"]
    )
    items = ItemSchema(many=True).dump(paginated_items.items)
    return jsonify(
        {
            "items": items,
            "items_per_page": paginated_items.per_page,
            "total_items": paginated_items.total,
        }
    )


@app.post("/categories/<int:category_id>/items")
@validate_token
@validate_input(ItemSchema)
@check_category_exist
def create_item(category, user_id, name, description, **__):
    existing_item = Item.query.filter_by(name=name).one_or_none()
    if existing_item:
        raise ItemExisted()

    new_item = Item(
        name=name, description=description, category_id=category.id, user_id=user_id
    )
    db.session.add(new_item)
    db.session.commit()

    return ItemSchema().jsonify(new_item)


@app.get("/categories/<int:category_id>/items/<int:item_id>")
@check_category_exist
@check_item_exist
def get_item(item, **__):
    return ItemSchema().jsonify(item)


@app.put("/categories/<int:category_id>/items/<int:item_id>")
@validate_token
@validate_input(ItemSchema)
@check_category_exist
@check_item_exist
def update_item(name, description, item, user_id, **__):
    if item.user_id != user_id:
        raise ItemUpdateForbidden()

    # check for existed item name
    existing_item = Item.query.filter_by(name=name).one_or_none()

    # if another item with input name existed
    if existing_item and existing_item.id != item.id:
        raise ItemExisted()

    item.name = name
    item.description = description
    db.session.commit()

    return jsonify({})


@app.delete("/categories/<int:category_id>/items/<int:item_id>")
@validate_token
@check_category_exist
@check_item_exist
def delete_item(item, user_id, **__):
    if item.user_id != user_id:
        raise ItemDeleteForbidden()

    db.session.delete(item)
    db.session.commit()

    return jsonify({})
