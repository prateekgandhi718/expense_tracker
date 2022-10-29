from rest_framework import serializers

class ExpenseSerializer(serializers.Serializer):
    category = serializers.CharField()
    date = serializers.DateField()
    amount = serializers.FloatField()
    comments = serializers.CharField()
    reciept = serializers.ImageField()

class ExpenseSerializerWithoutReciept(serializers.Serializer):
    category = serializers.CharField()
    date = serializers.DateField()
    amount = serializers.FloatField()
    comments = serializers.CharField()