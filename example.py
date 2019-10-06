from pyvaracl import ProtectedClass


def access_protected_test(instance):
    return instance._test


class MyClass(ProtectedClass):
    # _acl is a list of access control rules, processed from top to bottom
    # First rule to match gives the result of the action
    _acl = [
        # Permit the protected function to interact from outside the class
        {
            "filter": lambda attribute, attribute_name, action: True,
            "targets": {"function": [access_protected_test]},
            "allow": True,
        },
        # Deny everything from editing read-only attributes (ones with a ro prefix)
        {
            "filter": lambda attribute, attribute_name, action: attribute_name.startswith(
                "ro"
            )
            and action == "write",
            "targets": {},
            "allow": False,
        },
        # Deny everything outside from accessing private attributes (now they're *really* private)
        {
            "filter": lambda attribute, attribute_name, action: attribute_name.startswith(
                "_"
            ),
            "targets": {},
            "allow": False,
        },
        # Allow everything outside to access non-private attributes
        {
            "filter": lambda attribute, attribute_name, action: not attribute_name.startswith(
                "_"
            ),
            "targets": {},
            "allow": True,
        },
    ]
    _test = 1024
    test = 1
    ro_test = 256

    def get_test(self):
        return self.test


instance = MyClass()
# Access to .test is permitted as it's a public attribute (rule #4)
print("Public variable:", instance.test)
# Access to ._test is denied as it's a public attribute (rule #3)
print("Private variable:", instance._test)
# Access to ._test is permitted as it was selectively whitelisted (rule #1)
print(
    "Private variable via explicitly whitelisted function:",
    access_protected_test(instance),
)

# Access to .ro_test is permitted as it's a public attribute (rule #4)
print("Read-only (before setting):", instance.ro_test)
# Setting .ro_test is forbidden as it's a read-only attribute (rule #2)
instance.ro_test = -1
print("Read-only (before setting):", instance.ro_test)

# Access to .test is permitted as it's a public attribute (rule #4)
print("Non-read-only (before setting)", instance.test)
# Setting .test is permitted as there are no rules that forbid it
instance.test = 512
print("Non-read-only (after setting)", instance.test)
