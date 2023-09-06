from django.db.models import Q
from rest_framework import serializers

from .models import Plan, Category, Product, PlanProducts


class PlanSerializer(serializers.ModelSerializer):
    price = serializers.FloatField()

    class Meta:
        model = Plan
        fields = '__all__'

    def create(self, validated_data):
        if Plan.objects.filter(title_plan=validated_data['title_plan']).exists():
            raise serializers.ValidationError('Plan already exists', code='plan_exists')

        return Plan.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if 'title_plan' in validated_data:
            if Plan.objects.filter(~Q(id=instance.id), title_plan=validated_data['title_plan']).exists():
                raise serializers.ValidationError('Plan already exists', code='plan_exists')

        instance.title_plan = validated_data.get('title_plan', instance.title_plan)
        instance.price = validated_data.get('price', instance.price)

        instance.save()
        return instance


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True, )

    class Meta:
        model = Product
        fields = ['id', 'category', 'title_product', 'description', 'image_product']


class PlanProductSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = Plan
        fields = ['id', 'title_plan', 'price', 'installments', 'fee_amount', 'products']

    def get_products(self, obj: Plan):
        planproducts = PlanProducts.objects.filter(plan=obj).values_list('product_id', flat=True)
        products = Product.objects.filter(products__in=planproducts)
        return ProductSerializer(products, many=True).data


class ProductPlansSerializer(serializers.ModelSerializer):
    plans = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title_product', 'description', 'image_product', 'category', 'plans']

    def get_plans(self, obj: Product):
        planproducts = PlanProducts.objects.filter(product=obj).values_list('plan_id', flat=True)
        plans = Plan.objects.filter(plans__in=planproducts)
        return PlanSerializer(plans, many=True).data
