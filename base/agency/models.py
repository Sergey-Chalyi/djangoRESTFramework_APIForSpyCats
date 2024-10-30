from django.db import models

from django.db import models

class SpyCat(models.Model):
    """
    Model representing a spy cat.

    Attributes:
        name (CharField): The name of the spy cat.
        years_of_experience (PositiveIntegerField): The number of years the spy cat has been working.
        breed (CharField): The breed of the spy cat.
        salary (DecimalField): The salary of the spy cat.

    Methods:
        __str__(self): Returns the name of the spy cat.
    """
    name = models.CharField(max_length=100)
    years_of_experience = models.PositiveIntegerField()
    breed = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Mission(models.Model):
    """
    Model representing a mission.

    A mission is associated with a spy cat and can have multiple targets.

    Attributes:
        cat (OneToOneField): The spy cat associated with the mission.
        complete (BooleanField): Indicates whether the mission has been completed.
        created_at (DateTimeField): The date and time when the mission was created.

    Methods:
        __str__(self): Returns a string representation of the mission, including the name of the associated spy cat.

    """

    cat = models.OneToOneField(SpyCat, on_delete=models.CASCADE, blank=True, null=True)
    complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mission for {self.cat.name}"


class Target(models.Model):
    """
    Model representing a target.

    A target is associated with a mission and represents an objective that the spy cat needs to complete.

    Attributes:
        mission (ForeignKey): The mission associated with the target.
        name (CharField): The name of the target.
        country (CharField): The country where the target is located.
        notes (TextField): Additional notes about the target.
        complete (BooleanField): Indicates whether the target has been completed.

    Methods:
        __str__(self): Returns a string representation of the target, including the name of the associated mission.

    """

    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, related_name="targets")
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    notes = models.TextField(blank=True, null=True)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return f"Target: {self.name} for mission {self.mission}"
