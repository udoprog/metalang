#include "generated.hpp"

#include <iostream>
#include <boost/foreach.hpp>
#include <json/json.h>
#include <boost/scoped_ptr.hpp>

using namespace metalang;

int main(int argc, char* argv[])
{
  dynamic_list li;

  /* add one item */
  {
    slask::item it;
    it.set_name("This is a name");
    li.push_back(it);
    object* base = new_instance("slask.item");
    base->set("name", it);
    li.push_back(base);
  }

  slask::test3 t;

  /* set a field and associate list */
  {
    t.set_playlist1(true);
    t.set_list(li);
  }

  Json::Value root = to_json(&t);
  boost::scoped_ptr<object> base(from_json(root));

  {
    Json::Value root2 = to_json(base.get());
    Json::FastWriter writer;
    std::cout << writer.write(root2) << std::endl;
  }

  return 0;
}
