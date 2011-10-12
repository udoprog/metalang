namespace metalang {
  Json::Value to_json(object* message)
  {
    dynamic_map m = message->to_dynamic_map();
    return map_to_json(m);
  }

  Json::Value map_to_json(dynamic_map& map)
  {
    Json::Value root;

    dynamic_map::iterator it;
    for (it = map.begin(); it != map.end(); it++) {
      dynamic_pair dp = *it;

      switch (dp.second.type()) {
        case String:
          root[dp.first] = dp.second.as_string();
          break;
        case Integer:
          root[dp.first] = dp.second.as_integer();
          break;
        case Boolean:
          root[dp.first] = dp.second.as_boolean();
          break;
        case List:
          root[dp.first] = list_to_json(dp.second.as_list());
          break;
        case Object:
          root[dp.first] = to_json(dp.second.as_object());
          break;
        case Empty:
          root[dp.first] = Json::nullValue;
          break;
      }
    }

    return root;
  }

  Json::Value list_to_json(dynamic_list& list)
  {
    Json::Value root(Json::arrayValue);

    dynamic_list::iterator it;
    for (it = list.begin(); it != list.end(); it++) {
      dynamic d = *it;

      switch (d.type()) {
        case String:
          root.append(d.as_string());
          break;
        case Integer:
          root.append(d.as_integer());
          break;
        case Boolean:
          root.append(d.as_boolean());
          break;
        case List:
          root.append(list_to_json(d.as_list()));
          break;
        case Object:
          root.append(to_json(d.as_object()));
          break;
        case Empty:
          root.append(Json::nullValue);
          break;
      }
    }

    return root;
  }

  object* from_json(Json::Value& root)
  {
    if (!root.isObject()) {
      return NULL;
    }

    Json::Value null;

    Json::Value classType = root.get("__class__", null);

    if (!classType.isString()) {
      return NULL;
    }

    object* base = new_instance(classType.asString());
    dynamic_map map = json_to_map(root);
    base->from_dynamic_map(map);
    return base;
  }

  dynamic_map json_to_map(Json::Value& map)
  {
    dynamic_map m;

    Json::Value::Members members = map.getMemberNames();
    Json::Value::Members::iterator it;

    for (it = members.begin(); it != members.end(); it++)
    {
      std::string key = *it;

      if (key.compare("__class__") == 0) {
        continue;
      }

      Json::Value val = map[key];

      switch (val.type()) {
      case Json::stringValue:
        m.insert(dynamic_pair(key, val.asString()));
        break;
      case Json::intValue:
        m.insert(dynamic_pair(key, val.asInt()));
        break;
      case Json::booleanValue:
        m.insert(dynamic_pair(key, val.asBool()));
        break;
      case Json::objectValue:
        {
          object* b = from_json(val);
          m.insert(dynamic_pair(key, b));
        }
        break;
      case Json::arrayValue:
        {
          dynamic_list list = json_to_list(val);
          m.insert(dynamic_pair(key, list));
        }
        break;
      default:
        break;
      }
    }

    return m;
  }

  dynamic_list json_to_list(Json::Value& list)
  {
    dynamic_list l;

    for (unsigned int i = 0; i < list.size(); i++)
    {
      Json::Value val = list[i];

      switch (val.type()) {
      case Json::stringValue:
        l.push_back(val.asString());
        break;
      case Json::intValue:
        l.push_back(val.asInt());
        break;
      case Json::booleanValue:
        l.push_back(val.asBool());
        break;
      case Json::objectValue:
        {
          object* b = from_json(val);
          l.push_back(b);
        }
        break;
      case Json::arrayValue:
        {
          dynamic_list list = json_to_list(val);
          l.push_back(list);
        }
        break;
      default:
        break;
      }
    }

    return l;
  }
}
