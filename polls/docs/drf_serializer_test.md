## Kod testujący model Person
```
from polls.models import Person, Team, MONTHS, SHIRT_SIZES
from polls.serializers import PersonSerializer, TeamSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import io

person = Person(name='Adam', month_added=1)
serializerP = PersonSerializer(person)
serializerP.data
contentP = JSONRenderer().render(serializerP.data)
contentP
streamP = io.BytesIO(contentP)
dataP = JSONParser().parse(streamP)
deserializerP = PersonSerializer(data=dataP)
deserializerP.is_valid()
deserializerP.errors
```
## Kod testujący model Team
```
team = Team(name='Stomil Olsztyn', country='PL')
serializerT = TeamSerializer(team)
serializerT.data
contentT = JSONRenderer().render(serializerT.data)
contentT
streamT = io.BytesIO(contentT)
dataT = JSONParser().parse(streamT)
deserializerT = TeamSerializer(data=dataT)
deserializerT.is_valid()
deserializerT.errors



```