/* this is intended to be constructed into the dynamically generated header. */
/* BEGIN */
#include <boost/shared_ptr.hpp>
#include <string>
#include <map>
#include <list>
#include <set>
#include <stdexcept>

namespace metalang {
  typedef enum {
    Empty =      0x0,
    String =     0x10,
    Integer =    0x20,
    Boolean =    0x30,
    List =       0x50,
    Object =     0x60
  } dynamic_type;

  class dynamic;
  class object;

  typedef std::list<dynamic> dynamic_list;
  typedef std::map<std::string, dynamic> dynamic_map;
  typedef std::pair<std::string, dynamic> dynamic_pair;

  typedef object* (*generator_function)();
  typedef std::map<std::string, metalang::generator_function> generator_map;
  typedef std::pair<std::string, metalang::generator_function> generator_pair;

  class missing_field : public std::runtime_error {
   public:
    missing_field(const char* fieldname);
  };

  class dynamic
  {
  public:
    dynamic();
    dynamic(int i);
    dynamic(bool b);
    dynamic(const std::string& s);
    dynamic(const char* s);
    dynamic(const dynamic_list& list);
    dynamic(object*);

    template<typename T>
    dynamic(const T& object);

    dynamic_type type();

    std::string&  as_string();
    dynamic_list& as_list();
    object*       as_object();
    bool          as_boolean();
    int           as_integer();
    bool empty();
  private:
    dynamic_type _type;

    /* any object value must be reference counted to ensure it's not
     * freed. */
    boost::shared_ptr<void> _pointer_value;

    /* primitives are simply stored taking up some space */
    union {
      bool boolean;
      int  integer;
    } _value;
  };

  class object {
    public:
      virtual message_type type() const = 0;
      virtual const char* name() const = 0;
      dynamic get(std::string key);
      void set(std::string key, dynamic value);
      bool has(std::string key) const;
      dynamic_map to_dynamic_map() const;
      void from_dynamic_map(dynamic_map);
    private:
      dynamic_map _map;
  };

  object* new_instance(std::string name);
}
/* END */
