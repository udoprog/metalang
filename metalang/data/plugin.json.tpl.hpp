#include <json/json.h>

namespace metalang {
  Json::Value to_json(object*);
  Json::Value map_to_json(dynamic_map& map);
  Json::Value list_to_json(dynamic_list& list);
  object* from_json(Json::Value&);
  dynamic_map json_to_map(Json::Value&);
  dynamic_list json_to_list(Json::Value&);
}
