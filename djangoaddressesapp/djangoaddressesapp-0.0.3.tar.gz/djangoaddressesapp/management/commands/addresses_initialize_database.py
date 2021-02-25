import requests
from django.core.management.base import BaseCommand, CommandError
from ...models import Region, State, City

class Command(BaseCommand):
    help = 'Import regions, states and cities by IBGE api'

    def handle(self, *args, **options):
        
        # Import Regions
        self.stdout.write(self.style.NOTICE('Initializing regions import by IBGE api.'))
        response = requests.get('https://servicodados.ibge.gov.br/api/v1/localidades/regioes')
        data = response.json()

        for item in data:
            region = Region()
            region.pk = item.get("id")
            region.name = item.get("nome")
            region.acronym = item.get("sigla")
            region.save()
            
        self.stdout.write(self.style.SUCCESS('Completed regions import by IBGE api.'))

        # Import States
        self.stdout.write(self.style.NOTICE('Initializing states import by IBGE api.'))
        response = requests.get('https://servicodados.ibge.gov.br/api/v1/localidades/estados')
        data = response.json()

        for item in data:
            state = State()
            state.pk = item.get("id")
            state.name = item.get("nome")
            state.acronym = item.get("sigla")
            state.region = Region.objects.get(pk=item.get("regiao").get("id"))
            state.save()
        
        self.stdout.write(self.style.SUCCESS('Completed cities import by IBGE api.'))

        # Import Cities
        self.stdout.write(self.style.NOTICE('Initializing states import by IBGE api.'))
        response = requests.get('https://servicodados.ibge.gov.br/api/v1/localidades/municipios')
        data = response.json()

        for item in data:
            city = City()
            city.pk = item.get("id")
            city.name = item.get("nome")
            city.state = State.objects.get(pk=item.get("microrregiao").get("mesorregiao").get("UF").get("id"))
            city.save()

        self.stdout.write(self.style.SUCCESS('Completed cities import by IBGE api.'))