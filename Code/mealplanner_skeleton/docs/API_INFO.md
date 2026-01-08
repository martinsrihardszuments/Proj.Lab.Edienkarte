# Open Food Facts API - Informācija

## Kas ir Open Food Facts?

**Open Food Facts** ir brīva, atvērta datubāze ar pārtikas produktu informāciju no visas pasaules. Tas ir līdzīgs Wikipedia, bet produktiem.

- **Brīvs un bezmaksas** - nav nepieciešama API atslēga
- **Miljoni produktu** - no daudzām valstīm
- **Uzturvērtības dati** - kalorijas, olbaltumvielas, tauki, ogļhidrāti
- **Atvērts kods** - ikviens var izmantot

## API Endpoint

```
https://world.openfoodfacts.org/cgi/search.pl
```

## Kā izmantot API

### 1. Meklēšana pēc produkta nosaukuma

**Piemērs pieprasījums:**
```python
import requests

url = "https://world.openfoodfacts.org/cgi/search.pl"
params = {
    'search_terms': 'chicken breast',
    'search_simple': 1,
    'action': 'process',
    'json': 1,
    'page_size': 5,
    'sort_by': 'popularity'
}

response = requests.get(url, params=params)
data = response.json()

products = data.get('products', [])
for product in products:
    print(product.get('product_name'))
    print(product.get('nutriments', {}))
```

### 2. API Parametri

- `search_terms` - produkta nosaukums (piemēram: "chicken", "salmon", "rice")
- `search_simple` - vienkārša meklēšana (1 vai 0)
- `action` - darbība ("process")
- `json` - atgriezt JSON formātā (1)
- `page_size` - cik produktus atgriezt (1-100)
- `sort_by` - kārtot pēc ("popularity", "product_name", "created_t")

### 3. Atgrieztie dati

API atgriež JSON ar produktu informāciju:

```json
{
  "products": [
    {
      "product_name": "Chicken Breast",
      "product_name_en": "Chicken Breast",
      "nutriments": {
        "energy-kcal_100g": 165,
        "proteins_100g": 31.0,
        "fat_100g": 3.6,
        "carbohydrates_100g": 0.0
      },
      "brands": "Brand Name",
      "categories": "Meat, Poultry",
      ...
    }
  ],
  "count": 1,
  "page": 1,
  "page_size": 5
}
```

### 4. Uzturvērtības dati

Galvenie lauki `nutriments` objektā:
- `energy-kcal_100g` vai `energy-kcal` - kalorijas uz 100g
- `energy-kj_100g` vai `energy-kj` - kilodžouli (var pārvērst: kJ / 4.184 = kcal)
- `proteins_100g` vai `proteins` - olbaltumvielas (g uz 100g)
- `fat_100g` vai `fat` - tauki (g uz 100g)
- `carbohydrates_100g` vai `carbohydrates` - ogļhidrāti (g uz 100g)

## Kā es to izmantoju projektā

Skaties failu: `core/management/commands/import_from_api.py`

Galvenās funkcijas:
1. `get_product_from_api()` - iegūst produktu no API
2. `extract_nutrition_data()` - izvelk uzturvērtības datus
3. `estimate_price()` - novērtē cenu (API nav cenu datu)

## Piemērs: Testēšana ar curl

```bash
curl "https://world.openfoodfacts.org/cgi/search.pl?search_terms=chicken&action=process&json=1&page_size=1"
```

## Piemērs: Testēšana Python

```python
import requests

# Meklēt produktu
url = "https://world.openfoodfacts.org/cgi/search.pl"
params = {
    'search_terms': 'salmon',
    'action': 'process',
    'json': 1,
    'page_size': 1
}

response = requests.get(url, params=params)
data = response.json()

if data.get('products'):
    product = data['products'][0]
    print(f"Produkts: {product.get('product_name')}")
    
    nutriments = product.get('nutriments', {})
    print(f"Kalorijas: {nutriments.get('energy-kcal_100g', 'N/A')} kcal/100g")
    print(f"Olbaltumvielas: {nutriments.get('proteins_100g', 'N/A')} g/100g")
    print(f"Tauki: {nutriments.get('fat_100g', 'N/A')} g/100g")
    print(f"Ogļhidrāti: {nutriments.get('carbohydrates_100g', 'N/A')} g/100g")
```

## Oficiālā dokumentācija

- **Mājaslapa**: https://world.openfoodfacts.org/
- **API dokumentācija**: https://openfoodfacts.github.io/api-documentation/
- **GitHub**: https://github.com/openfoodfacts

## Ierobežojumi

⚠️ **Nav cenu datu** - API nesatur produktu cenas, tāpēc es novērtēju cenas pēc produkta veida

⚠️ **Datu kvalitāte** - daži produkti var būt ar nepilniem datiem

⚠️ **Rate limiting** - ieteicams būt pieklājīgam un nepieprasīt pārāk daudz vienlaikus

## Alternatīvas API

Ja vēlies citus API ar cenu datiem:

1. **USDA FoodData Central** - https://fdc.nal.usda.gov/api-guide.html
   - Pieprasa API atslēgu
   - Labi uzturvērtības dati
   - Nav cenu datu

2. **Edamam Food Database** - https://developer.edamam.com/food-database-api
   - Pieprasa API atslēgu
   - Nav cenu datu

3. **Spoonacular API** - https://spoonacular.com/food-api
   - Pieprasa API atslēgu
   - Ir cenu dati (bet maksas)

## Kā izmantot manu komandu

```bash
# Pievienot produktus no API
python manage.py import_from_api

# Pievienot konkrētus produktus
python manage.py import_from_api --products "chicken" "salmon" "rice"

# Aizstāt esošos produktus
python manage.py import_from_api --replace
```
