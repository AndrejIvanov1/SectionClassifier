import os


class DatasetSaver:
    def __init__(self, data_path):
        self.data_path = data_path
        self.abstract_path = os.path.join(data_path, "abstract")
        self.body_path = os.path.join(data_path, "body")
        self.sample_separator = os.linesep

        if not os.path.exists(self.abstract_path):
            os.mkdir(self.abstract_path)
        if not os.path.exists(self.body_path):
            os.mkdir(self.body_path)

    def save_abstract(self, abstract_sections):
        for title, content in abstract_sections.items():
            section_path = os.path.join(self.abstract_path, title)
            self.store_sample(section_path, content)

    def save_body(self, body_sections):
        for title, content in body_sections.items():
            section_path = os.path.join(self.body_path, title)
            self.store_sample(section_path, content)

    def store_sample(self, path, content):
        with open(path, 'a+', encoding='UTF-8') as f:
            try:
                f.write(content + self.sample_separator)
            except Exception as e:
                with open('errors', 'a+') as ef:
                    ef.write(path + self.sample_separator)

