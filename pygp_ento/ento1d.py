import warnings

class EntoLine(object):
    def __init__(self, max_length):
        self.min = 0
        self.max = max_length
        self.scale_factor = 2
        self.num_scales = 25
        self.buckets = 64

    def _scaled_index(self, num, scale):
        _range = self.max - self.min
        bucket_range = _range / self.buckets
        _size = _range / int(self.scale_factor**scale)
        bucket_size = bucket_range / int(self.scale_factor ** scale)
        min_scaled = self.min / int(self.scale_factor ** scale)
        _mod = num % _size
        try:
            _index = ((_mod + min_scaled) / bucket_size) % self.buckets
            return int(_index)
        except ZeroDivisionError:
            warnings.warn(RuntimeWarning("Too many scales for number. Some scales will never be used."))
            return int(0)

    def get_indexes(self, num):
        index_list = []
        for scale in range(self.num_scales):
            index_list.append(self._scaled_index(num, scale))
        return index_list

