global_keyDic = None
global_keys_down = None


class GlobalKeyCombinationDictionary:
    def __init__(self):
        global global_keyDic
        global_keyDic = {'RECALC': self.recalc_key_combination_dictionary}
        global global_keys_down
        global_keys_down = []

    def append_input_combinations(self, keydic):
        """Keydic must be a dictionary of vtk key strings containing either a keydic or a function"""
        global_keyDic.update(keydic)

    def recalc_key_combination_dictionary(self):
        global global_keys_down
        i = [0]
        key_dic = [global_keyDic]
        while True:
            try:
                if isinstance(key_dic[-1][global_keys_down[i[-1]]], dict):
                    key_dic.append(key_dic[-1][global_keys_down[i[-1]]])
                    i[-1] += 1
                    i.append(0)
                    continue
                elif callable(key_dic[-1][global_keys_down[i[-1]]]):
                    key_dic[-1][global_keys_down[i[-1]]]()
            except KeyError:
                pass
            except IndexError:
                pass
            if i[-1] < len(global_keys_down):
                i[-1] += 1
            elif len(i) > 1:
                i.pop()
                key_dic.pop()
            else:
                break

    def key_down(self, key):
        if key not in global_keys_down:
            global_keys_down.append(key)
            global_keyDic['RECALC']()

    def key_up(self, key):
        global_keys_down.remove(key)
