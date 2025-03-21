from rest_framework import serializers
from home.models import *
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["category_name"]

class AnimalBreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalBreed
        fields = ["animal_breed"]

class AnimalColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalColor
        fields = ["animal_color"]

class AnimalImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalImages
        fields = ["animal_images"]

class AnimalSerializer(serializers.ModelSerializer):
    animal_category = serializers.SerializerMethodField()
    animal_breed = AnimalBreedSerializer(many = True)
    animal_color = AnimalColorSerializer(many = True)
    #animal_images = AnimalImagesSerializer(many = True)

    
    def get_animal_category(self,obj):
        return obj.animal_category.category_name
    
    def create(self, data):
        # Extract animal_breed and animal_colour from data
        animal_breed_data = data.pop('animal_breed', []) 
        animal_color_data = data.pop('animal_color', [])  

        # Create the Animal object
        animal = Animal.objects.create(**data,animal_category = Category.objects.get(category_name = "Dog"))

        for breed in animal_breed_data:
            try:
                animal_breed_obj = AnimalBreed.objects.get(animal_breed=breed['animal_breed'])
                animal.animal_breed.add(animal_breed_obj)
            except AnimalBreed.DoesNotExist:
                raise ValueError(f"AnimalBreed with name '{breed['animal_breed']}' does not exist.")

        for color in animal_color_data:
            try:
                animal_color_obj = AnimalColor.objects.get(animal_color=color['animal_color'])
                animal.animal_color.add(animal_color_obj)
            except AnimalColor.DoesNotExist:
                raise ValueError(f"AnimalColor with name '{color['animal_color']}' does not exist.")

        return animal

    def update(self, instance, validated_data):
        # Update animal_breed
        if 'animal_breed' in validated_data:
            animal_breed_data = validated_data.pop('animal_breed', [])
            instance.animal_breed.clear()
            for breed in animal_breed_data:
                try:
                    animal_breed_obj = AnimalBreed.objects.get(animal_breed=breed['animal_breed'])
                    instance.animal_breed.add(animal_breed_obj)
                except AnimalBreed.DoesNotExist:
                    raise ValueError(f"AnimalBreed with name '{breed['animal_breed']}' does not exist.")

        # Update animal_color
        if 'animal_color' in validated_data:
            animal_color_data = validated_data.pop('animal_color', [])
            instance.animal_color.clear()
            for color in animal_color_data:
                try:
                    animal_color_obj = AnimalColor.objects.get(animal_color=color['animal_color'])
                    instance.animal_color.add(animal_color_obj)
                except AnimalColor.DoesNotExist:
                    raise ValueError(f"AnimalColor with name '{color['animal_color']}' does not exist.")

        # Update other fields
        instance.animal_name = validated_data.get('animal_name', instance.animal_name)
        instance.animal_description = validated_data.get('animal_description', instance.animal_description)
        instance.animal_gender = validated_data.get('animal_gender', instance.animal_gender)
        instance.save()

        return instance
    
    class Meta:
        model = Animal
        exclude = ["updated_at"]

class AnimalLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalLocation
        fields = '__all__'

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100, write_only=True)

    def validate(self, data):
        if User.objects.filter(username=data.get("username")).exists():
            raise serializers.ValidationError({"username": "Username already exists."})

        if User.objects.filter(email=data.get("email")).exists():
            raise serializers.ValidationError({"email": "Email already exists."})

        return data  # Always return the data after validation

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        email = validated_data['email']

        user = User.objects.create_user(username=username,password=password,email=email)
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=100, write_only=True)

    def validate(self, data):

        if 'username' in data:
            user = User.objects.filter(username = data['username'])
            if not user.exists():
                raise serializers.ValidationError("username doesnot exists")
        return data