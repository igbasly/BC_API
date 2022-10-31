from pydantic import BaseModel


class BaseModel(BaseModel):
    def dict(self, *args, **kwargs):
        params = super().dict(*args, **kwargs)
        new_dict = {}
        for key in params:
            if params[key] is not None:
                new_dict[key] = params[key]

        return new_dict

    @classmethod
    def get_attributes(cls: BaseModel):
        base_attr = cls.__fields__
        attrs = {}
        for key in base_attr:
            type_ = base_attr[key]._type_display()
            if "List" in type_:
                attrs[key] = []  # pragma: no cover
            elif "Dict" in type_:
                attrs[key] = {}  # pragma: no cover
            else:
                if base_attr[key].required:
                    attrs[key] = None
                else:
                    attrs[key] = base_attr[key].default
        return attrs
