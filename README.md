# poogle-nlp
NLP Tool for Poogle Project

poogle-nlp is a project for detecting intent from Turkish sentences. I have tried to used elasticsearch indexing for solving this problem. Project developers must set specific mappings to es given below.

##### Requirements
1. elasticsearch 1.6
2. poogle-auth (https://github.com/erhmutlu/poogle-auth)
3. django 1.8.5, djangorestframework 3.3.2
4. other requirements can be installed with `pip` from /service/etc/requirements/common.txt

##### Elasticsearch Documents
1. Entity

An entity is like a variable, it has 3 fields: entity_key, entity_synonyms, value. 
Example;
```json
{
    "entity_synonyms": ["İstanbul", "Megakent"],
    "value": "İstanbul",
    "entity_key":"@City"
}
```

According to above entity object, basically İstanbul and Megakent are `synonyms`. If in a sentence one of them appears, it will hit this entity object.

`value` field is for later calculations, for example a user can refer to İstanbul with Megakent, but thirdparty weather api's are waiting for İstanbul as a city request.

`entity_key` shows what this entity is. In this scenario the entity is a city.

2. Intent

An intent refers to actions of sentences system can understand or can make an inference.
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
Indexing all numbers as entities into elasticsearch is not convenient way, I have written a cool tool to detect numbers in sentence. It can be in numberical format, or word format, or mixed.

Now, this tool can detect at most `dokuz yüz doksan dokuz milyon dokuz yüz doksan dokuz bin dokuz yüz doksan dokuz` or its some mixed shape. But it can be developed to higher numbers later. However, there is not maximum limit to detect if the number contains only digits!

[/service/apps/defaultapp/tools/number](https://github.com/erhmutlu/poogle-nlp/blob/master/service/apps/defaultapp/tools/number.py)

##### Poogle-Nlp Algorithm
I will tell the algorithm by showing an example.

```
user request = "İstanbul'da 3 Nisan'da saat 16.45'te hava nasıl olacak ?" 
```
1. Clear Input
    Clear punctiation signs(:.,?)
    Clear extra whitespaces "  " -> " "
1. Detect Entities
    1. Firstly Detect Numbers
        ```
        [
            {
                "entity_synonyms": [3, u'3'],
                "value": 3,
                "entity_key": "@Number"
            },
            {
                "entity_synonyms": [16, u'16'],
                "value": 16,
                "entity_key": "@Number"
            },
            {
                "entity_synonyms": [45, u'45'],
                "value": 45,
                "entity_key": "@Number"
            }
        ]
        ```
    
    2. Detect Entities using Elasticsearch
        ```
        [
            {
                "entity_synonyms": ["Nisan"],
                "value": 4,
                "entity_key": "@Month"
            },
            {
                "entity_synonyms": ["İstanbul", "Megakent"],
                "value": "İstanbul",
                "entity_key": "@City"
            }
        ]
        ```
1. Eliminate entities from sentence
    entities will be used for query to `params` field of an intent. Non-entity part of sentence will be used for query to `sentence` field of an intent.
1. Query to Elasticsearch for Intent

    First Simple Rule:
        Entities MUST be match to params of intent.
        Other non-entity words MAY match or NOT.
    1. Exact Match
        ```python
        must = [Q('match', params=entity['key']) for entity in entities] if entities is not None else []
        should = [Q('match', sentence={"query": user_input, "operator": "and"})]

        query = Q('bool', must=must, should=should, minimum_should_match=len(should))
        ```
        In this query, `@City @Number @Month saat @Number @Number hava nasıl olacak` or some other combinations of words MUST be indexed.
        
        If any hit, TA DAA! we found matches. Then; `eliminates_intents_with_extra_params` Elasticsearch may hit to some documents with extra params like params["@City","@Number", "@Number", "@Number", "@Month", `"@Number"` ], we MUST eliminate those matches.
            
        If there is multiple intents left, `find_closest_match` using python difflib library.
        
        If there is no matched intent, go on with approximate match
    2. Approximate Match
        ```python
        inputs = perform_whitespace_tokenizer(user_input)
        should = [Q('match', sentence=input.strip()) for input in inputs]
        must = [Q('match', params=entity['key']) for entity in entitys] if entitys is not None else []
        
        min_should_match = IntentRecognitionService.__calculate_min_should_match(should)
        query = Q('bool', must=must, should=should, minimum_should_match=min_should_match)
        ```
        
        In this query, params is MUST again, but non-entity words are optional with some ratio(.75). For example,
        
        `@City @Number @Month saat @Number @Number hava nasıl olacak`. @City, 3 times @Number and @Month MUST be hit. Other words "saat", "hava", "nasıl", "olacak" may not be in sentence. In this case, .75 ratio is 3 words. Thus 1 word may not be in sentence.
        
        If any hit, TA DAA! we found matches. Then; `eliminates_intents_with_extra_params` Elasticsearch may hit to some documents with extra params like params["@City","@Number", "@Number", "@Number", "@Month", `"@Number"` ], we MUST eliminate those matches.
            
        If there is multiple intents left, `find_closest_match` using python difflib library.
        
3. If found a match reshape response!
    ```json
    {
        "id": "some_id_here",
        "action": "get_weather_by_city_date_hour",
        "sentence": "@City @Number @Month saat @Number @Number hava nasıl olacak",
        "original_sentence": "@City @Number @Month saat @Number @Number hava nasıl olacak",
        "params": ["@City","@Number", "@Number", "@Number", "@Month"]
    }
    ```
    
    put our entities intto response's params field.
    
    Result:
     ```json
    {
        "id": "some_id_here",
        "action": "get_weather_by_city_date_hour",
        "sentence": "@City @Number @Month saat @Number @Number hava nasıl olacak",
        "original_sentence": "@City @Number @Month saat @Number @Number hava nasıl olacak",
        "params": "above_entities_array!!!"
    }
    ```
    
    1. Look in to settings `SHAPER_CLASS_MAPPINGS` if there is a mapping for `get_weather_by_city_date_hour``
        
        YES ! `{'action': 'get_weather_by_city_date_hour', 'clz': 'Weather'},`
        
        Then, we must have `get_weather_by_city_date_hour` method in `Weather` class in `shapers` package.
        
        My implementation result is:
        
        ```json
        {
          "intent": {
            "action": "get_weather_by_city_date_hour",
            "params": {
              "date": "2016-04-03",
              "city": {
                "presentation_value": "İstanbul",
                "value": "İstanbul",
                "key": "@City"
              },
              "hour": "16:45"
            }
          },
          "class": "Weather"
        }
        ```
4. Simple! Return It!
        
    
