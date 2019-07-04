def customize_foldername(instance, filename):
    filename = instance.slug + '.' + filename.split('.')[1]
    return '{}/{}'.format(instance.slug, filename)
