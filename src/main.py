from fastapi import FastAPI, Body, Request

from e_com_test.src.db import forms_collection
from e_com_test.src.validators import is_date, is_email, is_phone_number

app = FastAPI()


def validate_form(dct: dict) -> dict:
    print(dct)
    for key, value in dct.items():
        if is_date(value):
            dct[key] = "date"
        elif is_phone_number(value):
            dct[key] = "phone"
        elif is_email(value):
            dct[key] = "email"
        else:
            dct[key] = "text"
    return dct


def find_form(templates: list[dict], validated_form: dict) -> dict | None:
    match_dict = {}
    for template in templates:
        template_name = template.pop("name")

        if set(template).issubset(set(validated_form)):
            match_dict.update({template_name: len(template)})

    return (
        {"template_name": max(match_dict, key=match_dict.get)} if match_dict else None
    )


@app.post("/get_form")
async def get_form_name(request: Request) -> dict:
    validated_form = validate_form(dict(request.query_params))
    dicts_list = [{key: value} for key, value in validated_form.items()]

    templates = await forms_collection.find({"$or": dicts_list}, {"_id": 0}).to_list(
        length=1000
    )
    if templates:
        form_name = find_form(templates, validated_form)
        return form_name if form_name else validated_form
    return validated_form


@app.post("/forms", status_code=201)
async def create_template(
    template: dict = Body(example={"f_name_1": "value_1", "f_name_2": "value_2"})
) -> dict:
    result = await forms_collection.insert_one(template)
    return {"template_id": str(result.inserted_id)}


@app.get("/forms")
async def get_templates() -> dict:
    templates = await forms_collection.find().to_list(length=1000)
    for template in templates:
        template["_id"] = str(template["_id"])
    return {"templates": templates}
