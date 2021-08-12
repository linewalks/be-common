def convert_query_to_response(attrs, elems):
  if isinstance(elems, list):
    return [{attr: col for attr, col in zip(attrs, elem)} for elem in elems]
  else:
    return {attr: col for attr, col in zip(attrs, elems)}
