## Kod testujący modele Person i Team

```
from polls.models import Person, Team, MONTHS, SHIRT_SIZES
from polls.serializers import PersonSerializer, TeamSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import io

person = Person(name='Adam', month_added=1)
team = Team(name='Stomil Olsztyn', country='PL')

serializerP = PersonSerializer(person)
serializerT = TeamSerializer(team)
serializerP.data
serializerT.data

contentP = JSONRenderer().render(serializerP.data)
contentT = JSONRenderer().render(serializerT.data)
contentP
contentT

streamP = io.BytesIO(contentP)
streamT = io.BytesIO(contentT)

dataP = JSONParser().parse(streamP)
dataT = JSONParser().parse(streamT)

deserializerP = PersonSerializer(data=dataP)
deserializerT = TeamSerializer(data=dataT)
deserializerP.is_valid()
deserializerT.is_valid()
```