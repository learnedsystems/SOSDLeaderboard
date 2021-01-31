from jinja2 import Environment, FileSystemLoader



env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('template.html')

output_from_parsed_template = template.render(indexes=indexes)
with open("index.html", "w") as filetowrite:
    filetowrite.write(output_from_parsed_template)