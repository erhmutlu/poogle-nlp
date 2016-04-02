# poogle-nlp
NLP Tool for Poogle Project

poogle-nlp is a project for detecting intent from turkish sentences. I have tried to used elasticsearch indexing for solving this problem. Project developers must set specific mappings to es given below.

##### Requirements
1. elasticsearch 1.6
2. poogle-auth (https://github.com/erhmutlu/poogle-auth)
3. django 1.8.5, djangorestframework 3.3.2
4. other requirements can be installed with `pip` from /service/etc/requirements/common.txt

##### Elasticsearch Documents
1. Entity

An entity is like a variable, it has 3 field: entity_key, entity_synonyms, value. 
Example;
```json
{
    "entity_synonyms": ["İstanbul", "Megakent"],
    "value": "İstanbul",
    "entity_key":"@City"
}
```

According to above entity object, basically İstanbul and Megakent are `synonym`. If in a sentence one of them appears, it will hit this entity object.

`value` field is for later calculations, for example a user can refer to İstanbul with Megakent, but thirdparty weather api's are waiting for İstanbul as a city request.

`entity_key` shows what this entity is. In this scenario the entity is a city.

2. Intent

An intent refers to sentences system can understand or can make an inference.
Example;

```json
{
    "sentence": "@City hava durumu nasıl olacak",
    "original_sentence": "@City hava durumu nasıl olacak",
    "action": "get_weather_by_city",
    "params": ["@City"]
}
```

`sentence` field is used for recognition purpose. It has specific filters and analyzers must defined in elasticsearch. If we look into value of `sentence` in this case, we see @City word. @City is actually a variable(entity), User can say any @City entity to match this sentence.

`original_sentence`: This field is used for creating a new intent as a admin to check if intent is already exist.

`action`: this field refers to the user's purpose. This action should be implemented in some class [here](https://github.com/erhmutlu/poogle-nlp/tree/master/service/apps/defaultapp/shapers), and should be added reference into settings.
```python
SHAPER_CLASS_MAPPINGS = [
    {'action': 'convert_currency_units', 'clz': 'Currency'},
    {'action': 'get_weather_by_city', 'clz': 'Weather'},
    {'action': 'get_weather_by_city_hour', 'clz': 'Weather'},
    {'action': 'get_weather_by_city_date', 'clz': 'Weather'},
    {'action': 'get_weather_by_city_date_hour', 'clz': 'Weather'},
    {'action': 'get_teams_match_score', 'clz': 'Score'},
    {'action': 'get_matches_of_week', 'clz': 'Score'},
    {'action': 'get_films_release_soon', 'clz': 'Movie'},
    {'action': 'get_films_released_already', 'clz': 'Movie'},
    {'action': 'get_films_released_this_week', 'clz': 'Movie'}
]
```
Program looks to `SHAPER_CLASS_MAPPINGS` if intent matches. These shaper classes shape response of the api. For example,

```
User requests:
sentence = "İstanbul'da hava durumu nasıl olacak"

Api response:
{
  "intent": {
    "action": "get_weather_by_city",
    "params": {
      "city": {
        "presentation_value": "İstanbul",
        "value": "İstanbul",
        "key": "@City"
      }
    }
  },
  "class": "Weather"
}
```

`params` field refers entities insided `sentence`.

##### Elasticsearch Mapping
[/service/etc/es/mapping.json](https://github.com/erhmutlu/poogle-nlp/blob/master/service/etc/es/mapping.json)

###### Deep into Elasticsearch Mapping

1. Shingle Filter (min:2, max:3)

    Shingle filter is used for matching entity key which means;
    ```
    entity_synonym -> Erhan Mutlu
    Erhan will not match to above synonym. Erhan Mutlu will be hit!
    ```

2. Apostrophe Filter

    User can say words with suffix. İstanbul'da and İstanbul words will be matched to İstanbul.
3. Turkish Stemmer Filter
4. Turkish Lowercase Filter
5. Asciifolding Filter


##### What about numbers ?
Indexing all numbers into elasticsearch is not convenient way, I have written a small tool to detect numbers in sentence. It can be in numberic format, or digital, or mixed.

Now, this tool can detect at most `dokuz yüz doksan dokuz milyon dokuz yüz doksan dokuz bin dokuz yüz doksan dokuz` or its some mixed shape. But it can be developed to higher numbers. Also, there is now maximum limit to detect if the number contains only digits!



