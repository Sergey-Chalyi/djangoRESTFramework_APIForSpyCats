import requests
from agency.models import Mission, Target, SpyCat
from rest_framework import serializers


class SpyCatSerializer(serializers.ModelSerializer):
    """
    Serializer for SpyCat model.

    This serializer is used to serialize and deserialize instances of the SpyCat model.

    Args:
        model (Model): The Django model to be serialized. In this case, it's the SpyCat model.
        fields (List[str]): A list of fields to be included in the serialization.

    Returns:
        Dict: A dictionary containing the serialized data of the SpyCat instance.
    """
    class Meta:
        model = SpyCat
        fields = ['name', 'years_of_experience', 'breed', 'salary']


class SpyCatCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new SpyCat instance.

    This serializer is used to validate and serialize the data for creating a new SpyCat instance.

    Args:
        model (Model): The Django model to be serialized. In this case, it's the SpyCat model.
        fields (List[str]): A list of fields to be included in the serialization.

    Returns:
        Dict: A dictionary containing the serialized data of the SpyCat instance.

    Raises:
        serializers.ValidationError: If the provided breed is not a valid breed.
    """
    class Meta:
        model = SpyCat
        fields = ['name', 'years_of_experience', 'breed', 'salary']

    def validate_breed(self, value):
        """
           Validates the provided breed for a SpyCat instance.

           Args:
               value (str): The breed to be validated.

           Raises:
               serializers.ValidationError: If the provided breed is not a valid breed.

           Returns:
               str: The validated breed.
        """
        # Validate breed using TheCatAPI
        # Make a request to TheCatAPI to get all valid cat breeds
        response = requests.get('https://api.thecatapi.com/v1/breeds')
        # Parse the response as JSON
        breeds = response.json()
        # Create a list of valid breeds with their names converted to lowercase
        valid_breeds = [breed['name'].lower() for breed in breeds]

        # Check if the provided breed is in the list of valid breeds
        if value.lower() not in valid_breeds:
            raise serializers.ValidationError(f"{value} is not a valid breed.")
        return value


class SpyCatUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating a SpyCat instance.

    This serializer is used to validate and serialize the data for updating a SpyCat instance.

    Args:
        model (Model): The Django model to be serialized. In this case, it's the SpyCat model.
        fields (List[str]): A list of fields to be included in the serialization.

    Returns:
        Dict: A dictionary containing the serialized data of the updated SpyCat instance.
    """
    class Meta:
        model = SpyCat
        fields = ['salary']



class TargetSerializer(serializers.ModelSerializer):
    """
    Serializer for Target model.

    This serializer is used to serialize and deserialize instances of the Target model.

    Args:
        model (Model): The Django model to be serialized. In this case, it's the Target model.
        fields (List[str]): A list of fields to be included in the serialization.

    Returns:
        Dict: A dictionary containing the serialized data of the Target instance.
    """
    class Meta:
        model = Target
        fields = ['id', 'name', 'country', 'notes', 'complete']


class MissionSerializer(serializers.ModelSerializer):
    """
    Serializer for Mission model.

    This serializer is used to serialize and deserialize instances of the Mission model.

    Args:
        model (Model): The Django model to be serialized. In this case, it's the Mission model.
        fields (List[str]): A list of fields to be included in the serialization.

    Returns:
        Dict: A dictionary containing the serialized data of the Mission instance.

    Methods:
        - create(validated_data): Creates a new Mission instance and associates it with its targets.
    """

    targets = TargetSerializer(many=True)

    class Meta:
        model = Mission
        fields = ['id', 'cat', 'complete', 'created_at', 'targets']

    def create(self, validated_data):
        """
        Creates a new Mission instance and associates it with its targets.

        Args:
            validated_data (Dict): A dictionary containing the validated data for the Mission instance.

        Returns:
            Mission: A newly created Mission instance.

        Raises:
            serializers.ValidationError: If the provided targets data is invalid.
        """
        # Get the list of targets data from the validated data
        targets_data = validated_data.pop('targets')
        # Create a new Mission instance with the provided data
        mission = Mission.objects.create(**validated_data)
        for target_data in targets_data:
            # Create a new Target instance for each target data and associate it with the newly created Mission instance
            Target.objects.create(mission=mission, **target_data)
        return mission


class TargetUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new SpyCat instance.

    This serializer is used to validate and serialize the data for creating a new SpyCat instance.

    Args:
        model (Model): The Django model to be serialized. In this case, it's the SpyCat model.
        fields (List[str]): A list of fields to be included in the serialization.

    Returns:
        Dict: A dictionary containing the serialized data of the SpyCat instance.

    Raises:
        serializers.ValidationError: If the provided breed is not a valid breed.
    """
    class Meta:
        model = Target
        fields = ['notes']

    def validate(self, attrs):
        """
           Validates the provided attributes for a Target instance.

           Args:
               attrs (Dict): A dictionary containing the attributes to be validated.

           Raises:
               serializers.ValidationError: If the target is already completed or if the associated mission is completed.

           Returns:
               Dict: The validated attributes.
        """
        # Get the target instance
        target = self.instance

        # Check if the target is complete
        if target.complete:
            raise serializers.ValidationError("Cannot update notes for a completed target.")

        # Check if the associated mission is complete
        if target.mission.complete:
            raise serializers.ValidationError("Cannot update notes for a target in a completed mission.")

        # Return the validated attributes
        return attrs

class TargetCompleteSerializer(serializers.ModelSerializer):
    """
    Serializer for marking a Target instance as completed.

    This serializer is used to validate and serialize the data for marking a Target instance as completed.

    Args:
        model (Model): The Django model to be serialized. In this case, it's the Target model.
        fields (List[str]): A list of fields to be included in the serialization.

    Returns:
        Dict: A dictionary containing the serialized data of the completed Target instance.

    Raises:
        serializers.ValidationError: If the target is already completed.
    """
    class Meta:
        model = Target
        fields = ['complete']


class MissionAssignCatSerializer(serializers.ModelSerializer):
    """
    Serializer for assigning a SpyCat to a Mission instance.

    This serializer is used to validate and serialize the data for assigning a SpyCat to a Mission instance.

    Args:
        model (Model): The Django model to be serialized. In this case, it's the Mission model.
        fields (List[str]): A list of fields to be included in the serialization.

    Returns:
        Dict: A dictionary containing the serialized data of the Mission instance with the assigned SpyCat.

    Raises:
        serializers.ValidationError: If the provided SpyCat instance is not valid.
    """
    class Meta:
        model = Mission
        fields = ['cat']


class MissionCompleteSerializer(serializers.ModelSerializer):
    """
    Serializer for marking a Mission instance as completed.

    This serializer is used to validate and serialize the data for marking a Mission instance as completed.

    Args:
        model (Model): The Django model to be serialized. In this case, it's the Mission model.
        fields (List[str]): A list of fields to be included in the serialization.

    Returns:
        Dict: A dictionary containing the serialized data of the completed Mission instance.

    Raises:
        serializers.ValidationError: If the mission is already completed.
    """
    class Meta:
        model = Mission
        fields = ['complete']
