# Translator

Translation Portal for Dataent Apps

### To add a new language

1. Add a new **Language** via desk
2. `bench use translate.epaas.com`
3. `bench translate-untranslated [language_code]`
4. Export new languages.json `bench execute dataent.core.doctype.language.language.export_languages_json` and commit it to the repo

> Use the Wikipedia page [List of ISO 639-1 codes](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) to look for the language code

### Update latest translations from apps

    bench import-source-messages

### Update missing translations

    bench translate-untranslated-all

### Copy translations from one language to another

    bench copy-language [from] [to]

### Export

**On Remote:**

    bench --site translate.epaas.com execute "translator.data.write_csv_for_all_languages"

**On local bench:**

    bench download-translations

