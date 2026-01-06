from django.core.management.base import BaseCommand
from core.models import Product
import requests
import time
import sys


def safe_print(text):
    """Safely print text that may contain Unicode characters"""
    try:
        return text.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding)
    except:
        return text.encode('ascii', errors='replace').decode('ascii')


class Command(BaseCommand):
    help = "Import real product data from Open Food Facts API"

    def add_arguments(self, parser):
        parser.add_argument(
            '--products',
            nargs='+',
            type=str,
            help='List of product names to search for',
            default=[
                # Breakfast foods
                'eggs', 'oats', 'greek yogurt', 'whole grain bread',
                # Protein sources
                'chicken breast', 'salmon', 'beef', 'turkey', 'tuna',
                # Carbs
                'brown rice', 'quinoa', 'pasta', 'potato', 'sweet potato',
                # Vitamins (vegetables and fruits)
                'spinach', 'broccoli', 'avocado', 'banana', 'apple', 
                'tomato', 'lettuce', 'carrot', 'orange'
            ]
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=5,
            help='Number of products to check per search term (default: 5)'
        )
        parser.add_argument(
            '--replace',
            action='store_true',
            help='Replace existing products with same name'
        )

    def get_product_from_api(self, search_term, limit=5):
        """Get product data from Open Food Facts API"""
        try:
            # Open Food Facts API endpoint
            url = "https://world.openfoodfacts.org/cgi/search.pl"
            params = {
                'search_terms': search_term,
                'search_simple': 1,
                'action': 'process',
                'json': 1,
                'page_size': limit,
                'sort_by': 'popularity'  # Get more popular/better quality products
            }
            
            try:
                self.stdout.write(f"Mekle: {search_term}...")
            except UnicodeEncodeError:
                self.stdout.write(f"Mekle: {safe_print(search_term)}...")
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            products = data.get('products', [])
            
            if not products:
                self.stdout.write(self.style.WARNING(f"Nav atrasts: {search_term}"))
                return None
            
            # Find product with best nutrition data
            best_product = None
            best_score = 0
            
            for product in products:
                nutriments = product.get('nutriments', {})
                # Score based on data completeness
                score = 0
                if nutriments.get('energy-kcal_100g') or nutriments.get('energy-kcal'):
                    score += 3
                if nutriments.get('proteins_100g') or nutriments.get('proteins'):
                    score += 2
                if nutriments.get('fat_100g') or nutriments.get('fat'):
                    score += 2
                if nutriments.get('carbohydrates_100g') or nutriments.get('carbohydrates'):
                    score += 2
                
                if score > best_score:
                    best_score = score
                    best_product = product
            
            return best_product if best_product else products[0]
            
        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f"API kļūda meklējot '{search_term}': {e}"))
            return None
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Kļūda: {e}"))
            return None

    def extract_nutrition_data(self, product_data):
        """Extract nutrition data from Open Food Facts product"""
        try:
            # Get product name
            name = product_data.get('product_name', '') or product_data.get('product_name_en', '')
            if not name:
                name = product_data.get('product_name_lt', '') or product_data.get('generic_name', 'Unknown Product')
            
            # Clean name (take first 120 chars, remove extra whitespace)
            name = ' '.join(name.split())[:120]
            
            # Get nutrition data per 100g
            nutriments = product_data.get('nutriments', {})
            
            # Energy in kcal (sometimes in kJ, need to convert)
            energy_kcal = nutriments.get('energy-kcal_100g') or nutriments.get('energy-kcal')
            if not energy_kcal:
                energy_kj = nutriments.get('energy-kj_100g') or nutriments.get('energy-kj')
                if energy_kj:
                    energy_kcal = energy_kj / 4.184  # Convert kJ to kcal
            
            # Macronutrients per 100g
            proteins = nutriments.get('proteins_100g') or nutriments.get('proteins') or 0
            fats = nutriments.get('fat_100g') or nutriments.get('fat') or 0
            carbs = nutriments.get('carbohydrates_100g') or nutriments.get('carbohydrates') or 0
            sugars = nutriments.get('sugars_100g') or nutriments.get('sugars') or 0
            
            # If energy is missing but we have macros, calculate it
            if not energy_kcal and (proteins or fats or carbs):
                energy_kcal = (proteins * 4) + (fats * 9) + (carbs * 4)
            
            # Estimate price (Open Food Facts doesn't have prices, so we estimate)
            # This is a simple estimation - in real app you'd use a price API
            price = self.estimate_price(name, energy_kcal or 0)
            
            # Convert energy to int safely
            try:
                kcal_int = int(float(energy_kcal)) if energy_kcal else 0
            except (ValueError, TypeError):
                kcal_int = 0
            
            return {
                'name': name,
                'kcal_100g': kcal_int,
                'p_g_100g': round(float(proteins), 1) if proteins else 0.0,
                'f_g_100g': round(float(fats), 1) if fats else 0.0,
                'c_g_100g': round(float(carbs), 1) if carbs else 0.0,
                'sugar_g_100g': round(float(sugars), 1) if sugars else 0.0,
                'price_eur_100g': round(price, 2),
                'category': self.classify_product(name)
            }
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Kļūda apstrādājot datus: {e}"))
            return None

    def classify_product(self, name):
        """Classify product into categories based on name"""
        name_lower = name.lower()
        
        # Breakfast foods
        if any(x in name_lower for x in ['egg', 'oat', 'yogurt', 'milk', 'cereal', 'muesli', 'granola']):
            return 'BREAKFAST'
        
        # Protein sources
        if any(x in name_lower for x in ['chicken', 'beef', 'pork', 'turkey', 'meat', 'salmon', 'fish', 'tuna', 'mackerel', 'tofu', 'tempeh']):
            return 'PROTEIN'
        
        # Carbs
        if any(x in name_lower for x in ['rice', 'pasta', 'potato', 'bread', 'quinoa', 'couscous', 'noodle']):
            return 'CARBS'
        
        # Vitamins (vegetables and fruits)
        if any(x in name_lower for x in ['vegetable', 'spinach', 'broccoli', 'carrot', 'lettuce', 'tomato', 'cucumber', 'pepper', 'salad', 'fruit', 'banana', 'apple', 'orange', 'berry', 'avocado']):
            return 'VITAMINS'
        
        return 'OTHER'

    def estimate_price(self, name, kcal):
        """Estimate price per 100g based on product type and calories"""
        name_lower = name.lower()
        
        # Price estimates in EUR per 100g
        if any(x in name_lower for x in ['chicken', 'poultry', 'turkey']):
            return 0.90
        elif any(x in name_lower for x in ['salmon', 'fish', 'tuna', 'mackerel']):
            return 2.00
        elif any(x in name_lower for x in ['beef', 'pork', 'meat']):
            return 1.30
        elif any(x in name_lower for x in ['yogurt', 'milk', 'dairy']):
            return 0.50
        elif any(x in name_lower for x in ['rice', 'pasta', 'grain', 'quinoa', 'oats']):
            return 0.20
        elif any(x in name_lower for x in ['bread', 'toast']):
            return 0.30
        elif any(x in name_lower for x in ['oil', 'olive']):
            return 1.10
        elif any(x in name_lower for x in ['nut', 'almond', 'seed']):
            return 1.50
        elif any(x in name_lower for x in ['vegetable', 'spinach', 'broccoli', 'carrot']):
            return 0.20
        elif any(x in name_lower for x in ['fruit', 'banana', 'apple', 'orange']):
            return 0.35
        elif any(x in name_lower for x in ['egg']):
            return 0.60
        elif any(x in name_lower for x in ['avocado']):
            return 0.90
        else:
            # Default estimate based on calories
            if kcal > 500:
                return 1.00
            elif kcal > 200:
                return 0.50
            else:
                return 0.30

    def handle(self, *args, **options):
        products_to_search = options['products']
        limit = options['limit']
        
        self.stdout.write(self.style.SUCCESS("=== Importē produktus no Open Food Facts API ==="))
        self.stdout.write(f"Meklē {len(products_to_search)} produktus...\n")
        
        imported = 0
        skipped = 0
        errors = 0
        
        for search_term in products_to_search:
            # Get product from API
            product_data = self.get_product_from_api(search_term, limit)
            
            if not product_data:
                errors += 1
                time.sleep(0.5)  # Rate limiting
                continue
            
            # Extract nutrition data
            nutrition = self.extract_nutrition_data(product_data)
            
            if not nutrition:
                errors += 1
                continue
            
            # Validate nutrition data before creating
            if not nutrition['name'] or nutrition['kcal_100g'] < 0:
                self.stdout.write(self.style.WARNING(f"Izlaists (nederīgi dati): {nutrition.get('name', 'Unknown')}"))
                skipped += 1
                continue
            
            # Check if product already exists
            existing = Product.objects.filter(name__iexact=nutrition['name']).first()
            if existing:
                if options.get('replace', False):
                    # Update existing product
                    for key, value in nutrition.items():
                        setattr(existing, key, value)
                    existing.save()
                    msg = f"[UPDATED] Atjaunots: {existing.name}"
                    try:
                        self.stdout.write(self.style.SUCCESS(msg))
                    except UnicodeEncodeError:
                        self.stdout.write(self.style.SUCCESS(safe_print(msg)))
                    imported += 1
                else:
                    msg = f"Jau eksiste: {nutrition['name']}"
                    try:
                        self.stdout.write(self.style.WARNING(msg))
                    except UnicodeEncodeError:
                        self.stdout.write(self.style.WARNING(safe_print(msg)))
                    skipped += 1
                continue
            
            # Create product
            try:
                product = Product.objects.create(**nutrition)
                msg = f"[OK] Pievienots: {product.name} ({product.kcal_100g} kcal, P:{product.p_g_100g}g F:{product.f_g_100g}g C:{product.c_g_100g}g, {product.price_eur_100g}EUR/100g)"
                try:
                    self.stdout.write(self.style.SUCCESS(msg))
                except UnicodeEncodeError:
                    self.stdout.write(self.style.SUCCESS(safe_print(msg)))
                imported += 1
            except Exception as e:
                error_msg = f"Neizdevas pievienot {nutrition['name']}: {str(e)}"
                try:
                    self.stdout.write(self.style.ERROR(error_msg))
                except UnicodeEncodeError:
                    self.stdout.write(self.style.ERROR(safe_print(error_msg)))
                errors += 1
            
            # Rate limiting - be nice to the API
            time.sleep(0.5)
        
        self.stdout.write("\n" + "="*50)
        self.stdout.write(self.style.SUCCESS(f"Gatavs! Importēts: {imported}, Izlaists: {skipped}, Kļūdas: {errors}"))
        self.stdout.write("="*50)
