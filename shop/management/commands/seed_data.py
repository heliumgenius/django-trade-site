import yaml
from pathlib import Path
from django.core.management.base import BaseCommand
from shop.models import Category, Product

class Command(BaseCommand):
    help = "Import sample categories and products"

    def handle(self, *args, **options):
        yaml_path = Path(__file__).resolve().parent.parent.parent.parent / "data" / "products.yaml"
        with open(yaml_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)

        for cat_data in data["categories"]:
            category, created = Category.objects.get_or_create(
                slug=cat_data["id"],
                defaults={
                    "name_zh": cat_data["name_zh"],
                    "name_en": cat_data["name_en"],
                    "order": Category.objects.count(),
                },
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Category: {category}"))
            for p in cat_data["products"]:
                product, created = Product.objects.get_or_create(
                    slug=p["slug"],
                    defaults={
                        "category": category,
                        "name_zh": p["name_zh"],
                        "name_en": p["name_en"],
                        "price": p["price"],
                        "stock": p["stock"],
                        "specs_zh": p.get("specs_zh", ""),
                        "specs_en": p.get("specs_en", ""),
                        "desc_zh": p.get("desc_zh", ""),
                        "desc_en": p.get("desc_en", ""),
                        "is_featured": True,
                        "is_active": True,
                    },
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"  Product: {product}"))
        self.stdout.write(self.style.SUCCESS("Seed complete!"))
