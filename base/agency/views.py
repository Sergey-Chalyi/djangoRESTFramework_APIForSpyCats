from rest_framework import generics, status
from rest_framework.response import Response
from .models import SpyCat, Mission, Target
from .serializers import SpyCatSerializer, SpyCatCreateSerializer, SpyCatUpdateSerializer, MissionSerializer, \
    MissionCompleteSerializer, MissionAssignCatSerializer, TargetCompleteSerializer, TargetUpdateSerializer


class SpyCatListView(generics.ListCreateAPIView):
    """
    View for listing and creating SpyCats.

    This view uses Django's built-in `ListCreateAPIView` to handle both GET and POST requests.

    GET requests will return a list of all SpyCats.

    POST requests will create a new SpyCat instance using the `SpyCatCreateSerializer`.

    Args:
        queryset (QuerySet): The queryset of SpyCat objects to be used.

    Returns:
        Response: A JSON response containing a list of SpyCat objects or a newly created SpyCat instance.

    Raises:
        HTTP 400 Bad Request: If the request method is not POST.
    """
    queryset = SpyCat.objects.all()

    def get_serializer_class(self):
        """
        Determines the appropriate serializer class to use based on the HTTP method of the request.

        Args:
            self (SpyCatListView): An instance of the SpyCatListView class.

        Returns:
            SpyCatCreateSerializer or SpyCatSerializer: The appropriate serializer class for the request.

        Raises:
            None
        """
        if self.request.method == 'POST':
            return SpyCatCreateSerializer
        return SpyCatSerializer


class SpyCatDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for updating and deleting a specific SpyCat instance.

    This view uses Django's built-in `RetrieveUpdateDestroyAPIView` to handle GET, PUT, and DELETE requests.

    GET requests will return a specific SpyCat instance.

    PUT requests will update a specific SpyCat instance using the `SpyCatUpdateSerializer`.

    DELETE requests will delete a specific SpyCat instance.

    Args:
        queryset (QuerySet): The queryset of SpyCat objects to be used.

    Returns:
        Response: A JSON response containing the updated or deleted SpyCat instance.

    Raises:
        HTTP 400 Bad Request: If the request method is not PUT or DELETE.
    """
    queryset = SpyCat.objects.all()
    serializer_class = SpyCatSerializer

    def update(self, request, *args, **kwargs):
        """
        Update a specific SpyCat instance.

        This method handles PUT requests.

        Args:
            request (Request): The HTTP request object.
            *args, **kwargs: Additional arguments and keyword arguments.

        Returns:
            Response: A JSON response containing the updated SpyCat instance.

        Raises:
            HTTP 400 Bad Request: If the request method is not PUT.
        """
        instance = self.get_object()
        # Get fields from the request
        salary = request.data.get('salary', None)

        # Check if there are changes other than the salary field
        if len(request.data) > 1 or (len(request.data) == 1 and salary is None):
            return Response({"error": "You can only update the salary."},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = SpyCatUpdateSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        """
        Patch for partial update of a specific SpyCat instance.

        This method handles PATCH requests.

        Args:
            request (Request): The HTTP request object.
            *args, **kwargs: Additional arguments and keyword arguments.

        Returns:
            Response: A JSON response containing the updated SpyCat instance.

        Raises:
            None
        """
        return self.update(request, *args, **kwargs)



class MissionListView(generics.ListCreateAPIView):
    """
    View for listing and creating Mission instances.

    This view uses Django's built-in `ListCreateAPIView` to handle both GET and POST requests.

    GET requests will return a list of all Mission objects.

    POST requests will create a new Mission instance using the `MissionSerializer`.

    Args:
        queryset (QuerySet): The queryset of Mission objects to be used.

    Returns:
        Response: A JSON response containing a list of Mission objects or a newly created Mission instance.

    Raises:
        HTTP 400 Bad Request: If the request method is not GET or POST.
    """
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer


class MissionDetailView(generics.RetrieveDestroyAPIView):
    """
    View for deleting a specific Mission instance.

    This view uses Django's built-in `RetrieveDestroyAPIView` to handle DELETE requests.

    DELETE requests will delete a specific Mission instance.

    Args:
        request (Request): The HTTP request object.
        *args, **kwargs: Additional arguments and keyword arguments.

    Returns:
        Response: A JSON response containing the deleted Mission instance.

    Raises:
        HTTP 400 Bad Request: If the request method is not DELETE.
        HTTP 400 Bad Request: If the Mission instance is assigned to a cat.
    """
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer

    def delete(self, request, *args, **kwargs):
        """
            Deletes a specific Mission instance.

            This method handles DELETE requests.

            Args:
                request (Request): The HTTP request object.
                *args, **kwargs: Additional arguments and keyword arguments.

            Returns:
                Response: A JSON response containing the deleted Mission instance.

            Raises:
                HTTP 400 Bad Request: If the request method is not DELETE.
                HTTP 400 Bad Request: If the Mission instance is assigned to a cat.
            """
        instance = self.get_object()
        if instance.cat:  # Check if mission is assigned to a cat
            return Response({"error": "Mission cannot be deleted because it is assigned to a cat."},
                            status=status.HTTP_400_BAD_REQUEST)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TargetUpdateView(generics.UpdateAPIView):
    """
    View for updating a specific Target instance.

    This view uses Django's built-in `UpdateAPIView` to handle PATCH and PUT requests.

    PATCH and PUT requests will update a specific Target instance using the `TargetUpdateSerializer`.

    Args:
        request (Request): The HTTP request object.
        *args, **kwargs: Additional arguments and keyword arguments.

    Returns:
        Response: A JSON response containing the updated Target instance.

    Raises:
        HTTP 400 Bad Request: If the request method is not PATCH or PUT.
        HTTP 400 Bad Request: If the Target instance is already completed.
    """
    queryset = Target.objects.all()
    serializer_class = TargetUpdateSerializer

    def patch(self, request, *args, **kwargs):
        """
        Patch for partial update of a specific Target instance.

        This method handles PATCH requests.

        Args:
            request (Request): The HTTP request object.
            *args, **kwargs: Additional arguments and keyword arguments.

        Returns:
            Response: A JSON response containing the updated Target instance.

        Raises:
            None
        """
        return self.update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        PUT for full update of a specific Target instance.

        This method handles PUT requests.

        Args:
            request (Request): The HTTP request object.
            *args, **kwargs: Additional arguments and keyword arguments.

        Returns:
            Response: A JSON response containing the updated Target instance.

        Raises:
            None
        """
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Update a specific Target instance.

        This method handles PATCH and PUT requests.

        Args:
            request (Request): The HTTP request object.
            *args, **kwargs: Additional arguments and keyword arguments.

        Returns:
            Response: A JSON response containing the updated Target instance.

        Raises:
            HTTP 400 Bad Request: If the request method is not PATCH or PUT.
            HTTP 400 Bad Request: If the Target instance is already completed.
        """
        target = self.get_object()
        if target.complete:  # Check if the target is complete
            return Response({"error": "Cannot update notes for a completed target."},
                            status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)


class TargetCompleteView(generics.UpdateAPIView):
    """
    View for marking a specific Target instance as completed.

    This view uses Django's built-in `UpdateAPIView` to handle PATCH requests.

    PATCH requests will mark a specific Target instance as completed.

    Args:
        request (Request): The HTTP request object.
        *args, **kwargs: Additional arguments and keyword arguments.

    Returns:
        Response: A JSON response containing the updated Target instance.

    Raises:
        HTTP 400 Bad Request: If the request method is not PATCH.
        HTTP 400 Bad Request: If the Target instance is already completed.
    """
    queryset = Target.objects.all()
    serializer_class = TargetCompleteSerializer

    def patch(self, request, *args, **kwargs):
        """
        Patch for marking a specific Target instance as completed.

        This method handles PATCH requests.

        Args:
            request (Request): The HTTP request object.
            *args, **kwargs: Additional arguments and keyword arguments.

        Returns:
            Response: A JSON response containing the updated Target instance.

        Raises:
            HTTP 400 Bad Request: If the request method is not PATCH.
            HTTP 400 Bad Request: If the Target instance is already completed.
        """
        target = self.get_object()
        target.complete = True
        target.save()
        return Response(TargetCompleteSerializer(target).data)


class MissionAssignCatView(generics.UpdateAPIView):
    """
       View for assigning a specific SpyCat instance to a Mission.

       This view uses Django's built-in `UpdateAPIView` to handle PATCH requests.

       PATCH requests will assign a specific SpyCat instance to a Mission. The `cat_id` parameter is used to identify the SpyCat instance to be assigned to the Mission. If the specified SpyCat instance does not exist, a `HTTP 404 Not Found` error is raised.

       Args:
           request (Request): The HTTP request object containing the data to be used for assigning a SpyCat instance to a Mission.
           *args, **kwargs: Additional arguments and keyword arguments that can be used to customize the behavior of the method.

       Returns:
           Response: A JSON response containing the updated Mission instance after the SpyCat instance has been assigned to it.

       Raises:
           HTTP 400 Bad Request: If the request method is not PATCH.
           HTTP 404 Not Found: If the specified SpyCat instance does not exist.

       Assigns a specific SpyCat instance to a Mission. The `cat_id` parameter is used to identify the SpyCat instance to be assigned to the Mission. If the specified SpyCat instance does not exist, a `HTTP 404 Not Found` error is raised.

       Parameters:
       - request (Request): The HTTP request object containing the data to be used for assigning a SpyCat instance to a Mission.
       - *args, **kwargs: Additional arguments and keyword arguments that can be used to customize the behavior of the method.

       Returns:
       - Response: A JSON response containing the updated Mission instance after the SpyCat instance has been assigned to it.

       Raises:
       - HTTP 400 Bad Request: If the request method is not PATCH.
       - HTTP 404 Not Found: If the specified SpyCat instance does not exist.
    """
    queryset = Mission.objects.all()
    serializer_class = MissionAssignCatSerializer

    def patch(self, request, *args, **kwargs):
        """
            Assign a specific SpyCat instance to a Mission.

            This method handles PATCH requests.

            Args:
                request (Request): The HTTP request object.
                *args, **kwargs: Additional arguments and keyword arguments.

            Returns:
                Response: A JSON response containing the updated Mission instance.

            Raises:
                HTTP 400 Bad Request: If the request method is not PATCH.
                HTTP 404 Not Found: If the specified SpyCat instance does not exist.

            Assigns a specific SpyCat instance to a Mission. The `cat_id` parameter is used to identify the SpyCat instance to be assigned to the Mission. If the specified SpyCat instance does not exist, a `HTTP 404 Not Found` error is raised.

            Parameters:
            - request (Request): The HTTP request object containing the data to be used for assigning a SpyCat instance to a Mission.
            - *args, **kwargs: Additional arguments and keyword arguments that can be used to customize the behavior of the method.

            Returns:
            - Response: A JSON response containing the updated Mission instance after the SpyCat instance has been assigned to it.

            Raises:
            - HTTP 400 Bad Request: If the request method is not PATCH.
            - HTTP 404 Not Found: If the specified SpyCat instance does not exist.
        """
        mission = self.get_object()
        cat_id = request.data.get('cat_id')
        try:
            cat = SpyCat.objects.get(id=cat_id)
            mission.cat = cat
            mission.save()
            return Response(MissionAssignCatSerializer(mission).data)
        except SpyCat.DoesNotExist:
            return Response({"error": "Cat not found."}, status=status.HTTP_404_NOT_FOUND)


# Отметить миссию как завершенную
class MissionCompleteView(generics.UpdateAPIView):
    """
    View for marking a specific Mission instance as completed.

    This view uses Django's built-in `UpdateAPIView` to handle PATCH requests.

    PATCH requests will mark a specific Mission instance as completed.

    Args:
        request (Request): The HTTP request object.
        *args, **kwargs: Additional arguments and keyword arguments.

    Returns:
        Response: A JSON response containing the updated Mission instance.

    Raises:
        HTTP 400 Bad Request: If the request method is not PATCH.
        HTTP 400 Bad Request: If the Mission instance is already completed.

    Marks a specific Mission instance as completed. The `patch` method handles PATCH requests. If all targets associated with the mission are already completed, the mission is marked as completed and a JSON response containing the updated mission instance is returned. If the mission is already completed, a `HTTP 400 Bad Request` error is raised.

    Parameters:
    - request (Request): The HTTP request object containing the data to be used for marking a Mission instance as completed.
    - *args, **kwargs: Additional arguments and keyword arguments that can be used to customize the behavior of the method.

    Returns:
    - Response: A JSON response containing the updated Mission instance.

    Raises:
    - HTTP 400 Bad Request: If the request method is not PATCH.
    - HTTP 400 Bad Request: If the Mission instance is already completed.
    """
    queryset = Mission.objects.all()
    serializer_class = MissionCompleteSerializer

    def patch(self, request, *args, **kwargs):
        """
           Marks a specific Mission instance as completed.

           This method handles PATCH requests. If all targets associated with the mission are already completed, the mission is marked as completed and a JSON response containing the updated mission instance is returned. If the mission is already completed, a `HTTP 400 Bad Request` error is raised.

           Args:
           - request (Request): The HTTP request object containing the data to be used for marking a Mission instance as completed.
           - *args, **kwargs: Additional arguments and keyword arguments that can be used to customize the behavior of the method.

           Returns:
           - Response: A JSON response containing the updated Mission instance.

           Raises:
           - HTTP 400 Bad Request: If the request method is not PATCH.
           - HTTP 400 Bad Request: If the Mission instance is already completed.
        """
        mission = self.get_object()
        if all(target.complete for target in mission.targets.all()):  # Проверка, завершены ли все цели
            mission.complete = True
            mission.save()
            return Response(MissionCompleteSerializer(mission).data)
        return Response({"error": "All targets must be completed to finish the mission."},
                        status=status.HTTP_400_BAD_REQUEST)

