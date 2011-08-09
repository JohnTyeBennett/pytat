from csv  import DictReader, DictWriter
from json import loads, dumps

class Metadata(object):

    @classmethod
    def from_string(cls, s):
        values = loads(s)
        obj = Metadata()
        for key in values.keys():
            setattr(obj, key, values[key])
        return obj

    def __str__(self):
        return dumps(self.__dict__)

class Store(object):

    def __init__(self, cls):
        self.cls      = cls
        self.entries  = []
        self.metadata = Metadata()

    fields = ()
    values_to_objects = {}
    fields_to_attributes = {}

    def __convert_value(self, field, value):
        if self.values_to_objects.has_key(field):
            return self.values_to_objects[field](value)
        else:
            return value

    def __translate_field_name(self, field):
        if self.fields_to_attributes.has_key(field):
            return self.fields_to_attributes[field]
        else:
            return field

    def __build_row(self, entry):
        row = {}
        for field in self.fields:
            row[field] = getattr(entry, self.__translate_field_name(field))
        return row

    def handle_metadata(self, metadata):
        self.metadata = metadata

    def load(self, input, filters = []):
        line = input.readline()
        if line.startswith('{'):
            self.handle_metadata(Metadata.from_string(line))
        else:
            input.seek(0)

        reader = DictReader(input)
        for row in reader:
            arguments = {}
            for field in self.fields:
                arguments[self.__translate_field_name(field)] = self.__convert_value(self.__translate_field_name(field), row[field])
            entry = self.cls(**arguments)
            if not filters or reduce(lambda a, b: a and b, [filter(entry) for filter in filters]):
                self.entries.append(self.cls(**arguments))

    def load_file(self, filename, filters = []):
        with open(filename) as f:
            self.load(f, filters)

    def save(self, output):
        if str(self.metadata) != '{}':
            output.write(str(self.metadata) + '\n')
        output.write(','.join(self.fields) + '\n')
        writer = DictWriter(output, self.fields)
        for entry in self.entries:
            writer.writerow(self.__build_row(entry))

    def save_file(self, filename):
        with open(filename, 'w') as f:
            self.save(f)
