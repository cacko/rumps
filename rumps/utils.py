from collections import OrderedDict

class ListDict(OrderedDict):
    def __insertion(self, link_prev, key_value):
        key, value = key_value
        if link_prev and isinstance(link_prev, list) and len(link_prev) > 2 and link_prev[2] != key:
            if key in self:
                del self[key]
            link_next = link_prev[1]
            self[key] = link_prev[1] = link_next[0] = [link_prev, link_next, key]
        dict.__setitem__(self, key, value)

    def insert_after(self, existing_key, key_value):
        self.__insertion(self[existing_key], key_value)

    def insert_before(self, existing_key, key_value):
        try:
            if self[existing_key] and isinstance(self[existing_key],  list):
                self.__insertion(self[existing_key][0], key_value)
            else:
                self.__insertion(self[existing_key], key_value)

        except:
            self.__insertion(self[existing_key], key_value)

