from collections import OrderedDict

class ListDict(OrderedDict):
    def __insertion(self, link_prev, key_value):
        key, value = key_value
        if link_prev[2] != key:
            if key in self:
                del self[key]
            link_next = link_prev[1]
            self[key] = link_prev[1] = link_next[0] = [link_prev, link_next, key]
        dict.__setitem__(self, key, value)

    def insert_after(self, existing_key, key_value):
        self.__insertion(self[existing_key], key_value)

    def insert_before(self, existing_key, key_value):
        try:
            self.__insertion(self[existing_key][0], key_value)
        except KeyError:
            self.__insertion(self[existing_key], key_value)

