from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List
from enum import Enum


class TaskType(Enum):
    """Enumeration of task types for pet care activities"""
    FEEDING = "feeding"
    WALK = "walk"
    MEDICATION = "medication"
    APPOINTMENT = "appointment"
    GROOMING = "grooming"
    TRAINING = "training"


@dataclass
class Pet:
    """Represents a pet in the PawPal+ system"""
    pet_id: str
    name: str
    species: str
    breed: str
    age: int
    health_info: str
    owner: 'Owner' = field(default=None)

    def record_feeding(self, time: datetime, amount: str) -> None:
        """Record a feeding activity for the pet"""
        pass

    def record_walk(self, time: datetime, duration: int) -> None:
        """Record a walk activity for the pet"""
        pass

    def add_medication(self, medication: str, schedule: str) -> None:
        """Add a medication to the pet's care routine"""
        pass

    def get_health_history(self) -> List['Activity']:
        """Retrieve the pet's activity/health history"""
        pass

    def update_health_info(self) -> None:
        """Update the pet's health information"""
        pass


@dataclass
class Task:
    """Represents a scheduled task in the PawPal+ system"""
    task_id: str
    task_type: TaskType
    pet: Pet
    due_time: datetime
    priority: int
    description: str
    completed: bool = False
    completed_time: datetime = field(default=None)
    recurrence: str = field(default=None)  # "daily", "weekly", or None

    def mark_complete(self, scheduler: 'Scheduler' = None) -> None:
        """Mark the task as completed and create next occurrence if recurring"""
        self.completed = True
        self.completed_time = datetime.now()
        
        if self.recurrence and scheduler:
            scheduler.create_next_occurrence(self)

    def update_priority(self, new_priority: int) -> None:
        """Update the task's priority level"""
        pass

    def postpone(self, new_time: datetime) -> None:
        """Reschedule the task to a new time"""
        pass

    def get_details(self) -> str:
        """Retrieve detailed information about the task"""
        pass


class Owner:
    """Represents a pet owner in the PawPal+ system"""

    def __init__(self, name: str, email: str, phone: str, address: str):
        """Initialize a new Owner"""
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.pets: List[Pet] = []
        self.scheduler: 'Scheduler' = None

    def add_pet(self, pet: Pet) -> bool:
        """
        Add a pet to the owner's collection.
        Returns True if pet was added, False if pet already exists (duplicate).
        Checks for duplicate by pet_id (primary key).
        """
        # Check if pet with this ID already exists
        if any(p.pet_id == pet.pet_id for p in self.pets):
            return False
        
        # Check if pet with this name already exists (warning)
        if any(p.name.lower() == pet.name.lower() for p in self.pets):
            return False
        
        self.pets.append(pet)
        return True

    def remove_pet(self, pet_id: str) -> bool:
        """
        Removes a pet from the owner by its pet_id.
        Returns True if pet was removed, False if pet not found.
        """
        original_length = len(self.pets)
        self.pets = [p for p in self.pets if p.pet_id != pet_id]
        return len(self.pets) < original_length

    def get_pets(self) -> List[Pet]:
        """Retrieve all pets owned by this owner"""
        return self.pets

    def update_profile(self) -> None:
        """Update the owner's profile information"""
        pass


class Scheduler:
    """Manages task scheduling and prioritization for pet care activities"""

    def __init__(self, scheduler_id: str, owner: Owner):
        """Initialize a new Scheduler"""
        self.scheduler_id = scheduler_id
        self.owner = owner
        self.tasks: List[Task] = []
        self.completed_tasks: List[Task] = []

    def add_task(self, task: Task) -> None:
        """Add a new task to the scheduler"""
        self.tasks.append(task)

    def generate_task_id(self) -> str:
        """Generate a task ID that does not collide with active or completed tasks."""
        existing_ids = {task.task_id for task in self.tasks}
        existing_ids.update(task.task_id for task in self.completed_tasks)

        next_index = 1
        while True:
            candidate = f"task_{next_index:03d}"
            if candidate not in existing_ids:
                return candidate
            next_index += 1

    def sort_by_time(self) -> List[Task]:
        """Sort all active tasks by due_time in chronological order"""
        return sorted(self.tasks, key=lambda task: task.due_time)

    def filter_tasks(self, pet_name: str = None, completed: bool = None) -> List[Task]:
        """Filter tasks by pet name and/or completion status"""
        filtered = self.tasks
        
        if pet_name is not None:
            filtered = [task for task in filtered if task.pet.name.lower() == pet_name.lower()]
        
        if completed is not None:
            filtered = [task for task in filtered if task.completed == completed]

        return sorted(filtered, key=lambda task: task.due_time)

    def create_next_occurrence(self, task: Task) -> None:
        """Create a new task for the next occurrence of a recurring task"""
        from datetime import timedelta
        
        # Calculate the next due time based on recurrence pattern
        if task.recurrence == "daily":
            next_time = task.due_time + timedelta(days=1)
        elif task.recurrence == "weekly":
            next_time = task.due_time + timedelta(weeks=1)
        else:
            return  # No valid recurrence pattern
        
        # Generate a new task ID (append a counter or timestamp)
        import time
        next_task_id = f"{task.task_id}__{int(time.time())}"
        
        # Create the new task with the same properties
        next_task = Task(
            task_id=next_task_id,
            task_type=task.task_type,
            pet=task.pet,
            due_time=next_time,
            priority=task.priority,
            description=task.description,
            completed=False,
            recurrence=task.recurrence
        )
        
        # Add the new task to the scheduler
        self.add_task(next_task)

    def detect_conflicts(self) -> List[str]:
        """
        Detect scheduling conflicts and return warning messages.
        Checks for:
        1. Same pet with multiple tasks at the same time (impossible)
        2. Different pets with tasks at the same time (owner can't do both simultaneously)
        Returns a list of warning messages (empty if no conflicts).
        """
        warnings = []
        
        # Only check active (incomplete) tasks
        active_tasks = [task for task in self.tasks if not task.completed]
        
        # Group tasks by their due_time
        time_groups = {}
        for task in active_tasks:
            time_key = task.due_time
            if time_key not in time_groups:
                time_groups[time_key] = []
            time_groups[time_key].append(task)
        
        # Check for conflicts within each time slot
        for due_time, tasks_at_time in time_groups.items():
            if len(tasks_at_time) > 1:
                # Check for same-pet conflicts (highest priority warning)
                pets_at_time = {}
                for task in tasks_at_time:
                    if task.pet.name not in pets_at_time:
                        pets_at_time[task.pet.name] = []
                    pets_at_time[task.pet.name].append(task)
                
                # Warning: Same pet with multiple tasks
                for pet_name, pet_tasks in pets_at_time.items():
                    if len(pet_tasks) > 1:
                        time_str = due_time.strftime('%Y-%m-%d %H:%M')
                        task_desc = ", ".join([t.task_type.value for t in pet_tasks])
                        warnings.append(
                            f"⚠️ CONFLICT: {pet_name} has multiple tasks at {time_str}: {task_desc}"
                        )
                
                # Warning: Multiple pets (owner can't do both)
                if len(pets_at_time) > 1:
                    time_str = due_time.strftime('%Y-%m-%d %H:%M')
                    pet_list = ", ".join(pets_at_time.keys())
                    warnings.append(
                        f"⚠️ OWNER CONFLICT: Multiple pets need attention at {time_str}: {pet_list}"
                    )
        
        return warnings

    def remove_task(self, task_id: str) -> bool:
        """Remove a task by ID from active/completed collections.

        Returns True if at least one task was removed, otherwise False.
        """
        before_active = len(self.tasks)
        before_completed = len(self.completed_tasks)

        self.tasks = [task for task in self.tasks if task.task_id != task_id]
        self.completed_tasks = [task for task in self.completed_tasks if task.task_id != task_id]

        return (len(self.tasks) < before_active) or (len(self.completed_tasks) < before_completed)

    def prioritize_tasks(self) -> List[Task]:
        """Organize and prioritize all active tasks"""
        pass

    def get_upcoming_tasks(self, days: int) -> List[Task]:
        """Retrieve tasks due within the specified number of days"""
        pass

    def complete_task(self, task_id: str) -> None:
        """Mark a task as completed"""
        pass

    def get_overdue_tasks(self) -> List[Task]:
        """Retrieve all overdue tasks"""
        pass

    def reschedule_task(self, task_id: str, new_time: datetime) -> None:
        """Reschedule an existing task.

        If the requested time conflicts with another active task, this method
        proposes the next available 15-minute slot and applies it.
        """
        target_task = next((task for task in self.tasks if task.task_id == task_id), None)
        if target_task is None:
            raise ValueError(f"Task '{task_id}' not found.")

        if target_task.completed:
            raise ValueError(f"Task '{task_id}' is completed and cannot be rescheduled.")

        candidate_time = new_time

        # Search up to 24 hours in 15-minute steps for the next conflict-free slot.
        max_attempts = int((24 * 60) / 15)
        attempts = 0
        while attempts <= max_attempts:
            has_conflict = any(
                other.task_id != task_id
                and not other.completed
                and other.due_time == candidate_time
                for other in self.tasks
            )
            if not has_conflict:
                target_task.due_time = candidate_time
                return

            candidate_time += timedelta(minutes=15)
            attempts += 1

        raise RuntimeError(
            f"Could not find an available time to reschedule task '{task_id}' within 24 hours."
        )


class Activity:
    """Represents a recorded activity or health event for a pet"""
    
    def __init__(self):
        """Initialize a new Activity"""
        pass
