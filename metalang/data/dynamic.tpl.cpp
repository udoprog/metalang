namespace metalang
{
  missing_field::missing_field(const char* fieldname) : std::runtime_error(fieldname)
  {
  }

  dynamic object::get(std::string key)
  {
    return _map[key];
  }

  void object::set(std::string key, dynamic value)
  {
    _map.insert(dynamic_pair(key, value));
  }

  bool object::has(std::string key) const
  {
    return _map.find(key) != _map.end();
  }

  dynamic_map object::to_dynamic_map() const
  {
    return _map;
  }

  void object::from_dynamic_map(dynamic_map map)
  {
    this->_map = map;
    this->_map["__class__"] = name();
  }

  dynamic::dynamic()
  {
    _type = Empty;
  }

  dynamic::dynamic(int i)
  {
    _value.integer = i;
    _type = Integer;
  }

  dynamic::dynamic(bool b)
  {
    _value.boolean = b;
    _type = Boolean;
  }

  dynamic::dynamic(const std::string& s)
  {
    _pointer_value.reset(new std::string(s));
    _type = String;
  }

  dynamic::dynamic(const char* s)
  {
    _pointer_value.reset(new std::string(s));
    _type = String;
  }

  dynamic::dynamic(const dynamic_list& list)
  {
    _pointer_value.reset(new dynamic_list(list));
    _type = List;
  }

  dynamic::dynamic(object* object)
  {
    _pointer_value.reset(object);
    _type = Object;
  }

  dynamic_type dynamic::type()
  {
    return _type;
  }

  bool dynamic::as_boolean()
  {
    return _value.boolean;
  }

  int dynamic::as_integer()
  {
    return _value.integer;
  }

  std::string& dynamic::as_string()
  {
    return *static_cast<std::string*>(_pointer_value.get());
  }

  dynamic_list& dynamic::as_list()
  {
    return *static_cast<dynamic_list*>(_pointer_value.get());
  }

  object* dynamic::as_object()
  {
    return static_cast<object*>(_pointer_value.get());
  }

  bool dynamic::empty()
  {
    return _type == Empty;
  }
}
