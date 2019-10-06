from pyvaracl import ProtectedClass


def access_protected_test(instance):
    return instance._test


class MyClass(ProtectedClass):
    _acl = [
        {
            "filter": lambda caller, attribute, attribute_name, action: True,
            "targets": {"function": [access_protected_test]},
            "action": "read",
            "allow": True,
        },
        {
            "filter": lambda caller, attribute, attribute_name, action: attribute_name.startswith(
                "_"
            ),
            "targets": {},
            "action": "read",
            "allow": False,
        },
        {
            "filter": lambda caller, attribute, attribute_name, action: not attribute_name.startswith(
                "_"
            ),
            "targets": {},
            "action": "read",
            "allow": True,
        },
    ]
    _test = 1024
    test = 1

    def get_test(self):
        return self.test


instance = MyClass()
print("Public variable:", instance.test)
print("Private variable:", instance._test)
print(
    "Private variable via explicitly whitelisted function:",
    access_protected_test(instance),
)
