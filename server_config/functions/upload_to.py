import os
from datetime import datetime
from unidecode import unidecode


def set_filename_format(now, filename):
    return "{date}-{microsecond}{extension}".format(
        date=str(now.date()),
        microsecond=now.microsecond,
        extension=os.path.splitext(filename)[1]
    )


def file_directory_path(instance, filename, **kwargs):
    path_final = "/{filename}"
    data = kwargs.get('data', [])

    directory = instance._meta.app_label.lower()
    model = instance._meta.verbose_name.lower()

    if directory.capitalize() != model.capitalize():
        pre_path_array = "{directory}/{model}"
    else:
        pre_path_array = "{model}"

    now = datetime.now()
    filename = set_filename_format(now, filename)

    for d in data:
        pre_path_array = pre_path_array + "/" + str(getattr(instance, d))

    pre_path_array = pre_path_array + path_final
    path = unidecode(pre_path_array.format(directory=directory, model=model, filename=filename))

    return path
