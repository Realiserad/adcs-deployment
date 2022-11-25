from ansible.module_utils.common.text.converters import to_text
from ansible.errors import AnsibleError

class FilterModule(object):
    def filters(self):
        return {
            'pronounce': self.pronounce
        }

    def pronounce(self, value):
        """
        Jinja2 filter for Ansible to pronounce positive numbers less than 13 in English.

        Example of usage in a Jinja2 template:
        {{ 13 | pronounce }} -> "13"
        {{ 12 | pronounce }} -> "twelve"
        {{ 0 | pronounce }} -> "zero"
        {{ -1 | pronounce }} -> AnsibleError("Cannot pronounce negative numbers.")

        :param value: value to be pronounced
        :return: the pronunciation of the value, or the number itself if the value is greater than 12
        :rtype: str
        :raises AnsibleError: if the value is negative or the value is not an integer
        """
        if value < 0:
            raise AnsibleError("Cannot pronounce negative numbers.")
        try:
            pronounciation = {
                0: "zero",
                1: "one",
                2: "two",
                3: "three",
                4: "four",
                5: "five",
                6: "six",
                7: "seven",
                8: "eight",
                9: "nine",
                10: "ten",
                11: "eleven",
                12: "twelve",
            }.get(int(value)) or value
            return to_text(pronounciation)
        except ValueError:
            raise AnsibleError('Cannot parse ' + value + ' as an integer.')