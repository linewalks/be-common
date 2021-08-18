def convert_cls_to_response(attrs, cls):
  return {attr: getattr(cls, attr) for attr in attrs}


def convert_query_to_response(attrs, elems, cls=None):
  if isinstance(elems, list):
    response_list = []
    for elem in elems:
      if cls is not None and isinstance(elem, cls):
        response_list.append(convert_cls_to_response(attrs, elem))
      else:
        response_list.append({attr: col for attr, col in zip(attrs, elem)})
    return response_list
  else:
    response = None
    if cls is not None and isinstance(elems, cls):
      response = convert_cls_to_response(attrs, elems)
    else:
      response = {attr: col for attr, col in zip(attrs, elems)}
    return response
