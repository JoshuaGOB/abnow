# call this function using python manage.py bulk_exports.property to upload json and images to AWS bucket
import json
import os
from django.core.management.base import BaseCommand
from django.core.files import File
from abnow.models import Image, Category, SubCategory

class Command(BaseCommand):
    help = 'Uploads data from a JSON file'

    def handle(self, *args, **kwargs):
        try:
            with open('mydata.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR('Could not find the JSON file.'))
            return
        except json.JSONDecodeError:
            self.stderr.write(self.style.ERROR('Could not parse the JSON file.'))
            return
        
        for image_data in data:
            for image_name, categories in image_data.items():
                image, created = Image.objects.get_or_create(name=image_name)
                
                if created:
                    try:
                        with open(os.path.join('path/to/images', image_name), 'rb') as img_file:
                            image.image.save(image_name, File(img_file), save=True)
                    except FileNotFoundError:
                        self.stderr.write(self.style.ERROR(f'Could not find an image for {image_name}.'))
                        image.delete()  # Remove the Image instance if its image file couldn't be found.
                        continue

                for category_name, sub_categories in categories['Codes'].items():
                    category, _ = Category.objects.get_or_create(name=category_name, image=image)
                    
                    for sub_category_name in sub_categories.keys():
                        SubCategory.objects.get_or_create(name=sub_category_name, category=category)
                        
        self.stdout.write(self.style.SUCCESS('Data uploaded successfully'))
