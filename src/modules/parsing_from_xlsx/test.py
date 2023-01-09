import wikipedia

wikipedia.set_lang('ru')

result = wikipedia.WikipediaPage('Балаклава').html()

print(result)

