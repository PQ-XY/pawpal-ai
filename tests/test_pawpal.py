import pytest
from datetime import datetime, timedelta
from pawpal_system import Owner, Pet, Scheduler, Task, TaskType


@pytest.fixture
def owner():
    """Create a test owner"""
    return Owner(
        name="Test Owner",
        email="test@example.com",
        phone="555-1234",
        address="123 Test St"
    )


@pytest.fixture
def pet(owner):
    """Create a test pet"""
    return Pet(
        pet_id="pet_001",
        name="Buddy",
        species="Dog",
        breed="Labrador",
        age=3,
        health_info="Healthy",
        owner=owner
    )


@pytest.fixture
def scheduler(owner):
    """Create a test scheduler"""
    return Scheduler(scheduler_id="sched_001", owner=owner)


@pytest.fixture
def task(pet):
    """Create a test task"""
    return Task(
        task_id="task_001",
        task_type=TaskType.FEEDING,
        pet=pet,
        due_time=datetime.now() + timedelta(hours=1),
        priority=2,
        description="Feed Buddy",
        completed=False
    )


class TestTaskCompletion:
    """Test suite for task completion functionality"""
    
    def test_mark_complete_changes_status(self, task):
        """Verify that mark_complete() changes the task's completed status"""
        # Initially task should not be completed
        assert task.completed is False
        assert task.completed_time is None
        
        # Call mark_complete (to be implemented)
        task.mark_complete()
        
        # After calling mark_complete, task should be completed
        assert task.completed is True
        assert task.completed_time is not None
        assert isinstance(task.completed_time, datetime)
    
    def test_completed_time_is_set_on_mark_complete(self, task):
        """Verify that completed_time is set when task is marked complete"""
        before_completion = datetime.now()
        task.mark_complete()
        after_completion = datetime.now()
        
        # completed_time should be set and be current
        assert task.completed_time is not None
        assert before_completion <= task.completed_time <= after_completion


class TestTaskAddition:
    """Test suite for task addition functionality"""
    
    def test_adding_task_to_scheduler(self, scheduler, task):
        """Verify that adding a task to scheduler is tracked"""
        # Initially scheduler should have no tasks
        assert len(scheduler.tasks) == 0
        
        # Add task to scheduler
        scheduler.add_task(task)
        
        # Scheduler should now have the task
        assert len(scheduler.tasks) == 1
        assert task in scheduler.tasks
    
    def test_task_associated_with_correct_pet(self, scheduler, pet, task):
        """Verify that added task is correctly associated with the pet"""
        # Add task to scheduler
        scheduler.add_task(task)
        
        # Task should reference the correct pet
        assert task.pet == pet
        assert task.pet.name == "Buddy"
    
    def test_multiple_tasks_for_same_pet(self, scheduler, pet):
        """Verify that multiple tasks can be added for the same pet"""
        # Create multiple tasks for the same pet
        task_1 = Task(
            task_id="task_001",
            task_type=TaskType.FEEDING,
            pet=pet,
            due_time=datetime.now() + timedelta(hours=1),
            priority=2,
            description="Morning feeding",
            completed=False
        )
        task_2 = Task(
            task_id="task_002",
            task_type=TaskType.WALK,
            pet=pet,
            due_time=datetime.now() + timedelta(hours=4),
            priority=2,
            description="Afternoon walk",
            completed=False
        )
        
        # Add both tasks to scheduler
        scheduler.add_task(task_1)
        scheduler.add_task(task_2)
        
        # Verify both tasks are in scheduler
        assert len(scheduler.tasks) == 2
        
        # Verify both tasks reference the same pet
        pet_tasks = [t for t in scheduler.tasks if t.pet == pet]
        assert len(pet_tasks) == 2
    
    def test_multiple_pets_multiple_tasks(self, scheduler, owner):
        """Verify that tasks can be added for multiple pets"""
        # Create two pets
        dog = Pet(
            pet_id="pet_001",
            name="Max",
            species="Dog",
            breed="Golden Retriever",
            age=5,
            health_info="Healthy",
            owner=owner
        )
        cat = Pet(
            pet_id="pet_002",
            name="Luna",
            species="Cat",
            breed="Siamese",
            age=3,
            health_info="Healthy",
            owner=owner
        )
        
        # Create tasks for each pet
        task_dog = Task(
            task_id="task_001",
            task_type=TaskType.WALK,
            pet=dog,
            due_time=datetime.now() + timedelta(hours=1),
            priority=2,
            description="Walk Max",
            completed=False
        )
        task_cat = Task(
            task_id="task_002",
            task_type=TaskType.MEDICATION,
            pet=cat,
            due_time=datetime.now() + timedelta(hours=2),
            priority=1,
            description="Luna's medication",
            completed=False
        )
        
        # Add tasks to scheduler
        scheduler.add_task(task_dog)
        scheduler.add_task(task_cat)
        
        # Verify both tasks are in scheduler
        assert len(scheduler.tasks) == 2
        
        # Verify tasks are associated with correct pets
        dog_tasks = [t for t in scheduler.tasks if t.pet == dog]
        cat_tasks = [t for t in scheduler.tasks if t.pet == cat]
        assert len(dog_tasks) == 1
        assert len(cat_tasks) == 1
        assert dog_tasks[0].pet.name == "Max"
        assert cat_tasks[0].pet.name == "Luna"


class TestSortingAndFiltering:
    """Test suite for sorting and filtering functionality"""
    
    def test_sort_empty_list(self, scheduler):
        """Sorting empty scheduler should return empty list"""
        result = scheduler.sort_by_time()
        assert result == []
    
    def test_sort_single_task(self, scheduler, task):
        """Sorting single task should return list with that task"""
        scheduler.add_task(task)
        result = scheduler.sort_by_time()
        assert len(result) == 1
        assert result[0] == task
    
    def test_sort_chronological_order(self, scheduler, pet):
        """Tasks should be sorted in chronological order by due_time"""
        # Create tasks in reverse chronological order
        task_1 = Task(
            task_id="task_1",
            task_type=TaskType.FEEDING,
            pet=pet,
            due_time=datetime.now() + timedelta(hours=3),
            priority=2,
            description="Third task",
            completed=False
        )
        task_2 = Task(
            task_id="task_2",
            task_type=TaskType.WALK,
            pet=pet,
            due_time=datetime.now() + timedelta(hours=1),
            priority=2,
            description="First task",
            completed=False
        )
        task_3 = Task(
            task_id="task_3",
            task_type=TaskType.MEDICATION,
            pet=pet,
            due_time=datetime.now() + timedelta(hours=2),
            priority=1,
            description="Second task",
            completed=False
        )
        
        # Add tasks in non-chronological order
        scheduler.add_task(task_1)
        scheduler.add_task(task_2)
        scheduler.add_task(task_3)
        
        # Sort and verify order
        sorted_tasks = scheduler.sort_by_time()
        assert sorted_tasks[0].task_id == "task_2"  # Earliest
        assert sorted_tasks[1].task_id == "task_3"  # Middle
        assert sorted_tasks[2].task_id == "task_1"  # Latest
    
    def test_filter_no_matches_pet_name(self, scheduler, pet):
        """Filter for non-existent pet returns empty list"""
        scheduler.add_task(Task(
            task_id="t1",
            task_type=TaskType.FEEDING,
            pet=pet,
            due_time=datetime.now() + timedelta(hours=1),
            priority=2,
            description="Test",
            completed=False
        ))
        
        result = scheduler.filter_tasks(pet_name="NonExistentPet")
        assert result == []
    
    def test_filter_case_insensitive(self, scheduler, pet):
        """Filter by pet name should be case-insensitive"""
        scheduler.add_task(Task(
            task_id="t1",
            task_type=TaskType.FEEDING,
            pet=pet,
            due_time=datetime.now() + timedelta(hours=1),
            priority=2,
            description="Test",
            completed=False
        ))
        
        # Test different cases
        result_lower = scheduler.filter_tasks(pet_name="buddy")
        result_upper = scheduler.filter_tasks(pet_name="BUDDY")
        result_mixed = scheduler.filter_tasks(pet_name="BuDdY")
        
        assert len(result_lower) == 1
        assert len(result_upper) == 1
        assert len(result_mixed) == 1
    
    def test_filter_by_completed_status(self, scheduler, pet):
        """Filter by completion status should separate completed and pending"""
        task_incomplete = Task(
            task_id="t1",
            task_type=TaskType.FEEDING,
            pet=pet,
            due_time=datetime.now() + timedelta(hours=1),
            priority=2,
            description="Incomplete",
            completed=False
        )
        task_complete = Task(
            task_id="t2",
            task_type=TaskType.WALK,
            pet=pet,
            due_time=datetime.now() + timedelta(hours=2),
            priority=2,
            description="Complete",
            completed=True
        )
        
        scheduler.add_task(task_incomplete)
        scheduler.add_task(task_complete)
        
        # Filter for incomplete
        incomplete = scheduler.filter_tasks(completed=False)
        assert len(incomplete) == 1
        assert incomplete[0].task_id == "t1"
        
        # Filter for complete
        complete = scheduler.filter_tasks(completed=True)
        assert len(complete) == 1
        assert complete[0].task_id == "t2"
    
    def test_filter_pet_and_status_combined(self, scheduler, owner):
        """Filter by both pet name and completion status"""
        dog = Pet(pet_id="p1", name="Max", species="Dog", breed="Lab", age=3, health_info="Healthy", owner=owner)
        cat = Pet(pet_id="p2", name="Luna", species="Cat", breed="Siamese", age=2, health_info="Healthy", owner=owner)
        
        t1 = Task(task_id="t1", task_type=TaskType.FEEDING, pet=dog, due_time=datetime.now() + timedelta(hours=1), priority=2, description="T1", completed=False)
        t2 = Task(task_id="t2", task_type=TaskType.WALK, pet=dog, due_time=datetime.now() + timedelta(hours=2), priority=2, description="T2", completed=True)
        t3 = Task(task_id="t3", task_type=TaskType.MEDICATION, pet=cat, due_time=datetime.now() + timedelta(hours=3), priority=1, description="T3", completed=False)
        
        scheduler.add_task(t1)
        scheduler.add_task(t2)
        scheduler.add_task(t3)
        
        # Max's incomplete tasks
        result = scheduler.filter_tasks(pet_name="Max", completed=False)
        assert len(result) == 1
        assert result[0].task_id == "t1"


class TestRecurringTasks:
    """Test suite for recurring task functionality"""
    
    def test_non_recurring_no_next_occurrence(self, scheduler, pet):
        """Completing non-recurring task should NOT create next occurrence"""
        task = Task(
            task_id="t1",
            task_type=TaskType.FEEDING,
            pet=pet,
            due_time=datetime.now() + timedelta(hours=1),
            priority=2,
            description="Feed",
            completed=False,
            recurrence=None
        )
        scheduler.add_task(task)
        
        task.mark_complete(scheduler)
        
        # Should still have just 1 task (the completed one)
        assert len(scheduler.tasks) == 1
        assert scheduler.tasks[0].completed is True
    
    def test_daily_task_creates_next_occurrence(self, scheduler, pet):
        """Daily recurring task should generate next occurrence when marked complete"""
        now = datetime(2026, 3, 31, 8, 0, 0)
        task = Task(
            task_id="t1",
            task_type=TaskType.FEEDING,
            pet=pet,
            due_time=now,
            priority=2,
            description="Daily feed",
            completed=False,
            recurrence="daily"
        )
        scheduler.add_task(task)
        
        task.mark_complete(scheduler)
        
        # Should have original (completed) + new task
        assert len(scheduler.tasks) == 2
        
        # Find the new incomplete task
        new_tasks = [t for t in scheduler.tasks if not t.completed]
        assert len(new_tasks) == 1
        assert new_tasks[0].due_time == datetime(2026, 4, 1, 8, 0, 0)
    
    def test_weekly_task_creates_next_occurrence(self, scheduler, pet):
        """Weekly recurring task should generate next occurrence exactly 7 days later"""
        now = datetime(2026, 3, 31, 10, 0, 0)
        task = Task(
            task_id="t1",
            task_type=TaskType.GROOMING,
            pet=pet,
            due_time=now,
            priority=2,
            description="Weekly groom",
            completed=False,
            recurrence="weekly"
        )
        scheduler.add_task(task)
        
        task.mark_complete(scheduler)
        
        # Should have original (completed) + new task
        assert len(scheduler.tasks) == 2
        
        # Find the new incomplete task
        new_tasks = [t for t in scheduler.tasks if not t.completed]
        assert len(new_tasks) == 1
        assert new_tasks[0].due_time == datetime(2026, 4, 7, 10, 0, 0)
    
    def test_recurring_task_preserves_properties(self, scheduler, pet):
        """New recurring task should inherit properties from original"""
        now = datetime(2026, 3, 31, 8, 0, 0)
        task = Task(
            task_id="t1",
            task_type=TaskType.MEDICATION,
            pet=pet,
            due_time=now,
            priority=1,
            description="Daily medication",
            completed=False,
            recurrence="daily"
        )
        scheduler.add_task(task)
        
        task.mark_complete(scheduler)
        
        new_task = [t for t in scheduler.tasks if not t.completed][0]
        
        # Verify properties match
        assert new_task.task_type == TaskType.MEDICATION
        assert new_task.priority == 1
        assert new_task.description == "Daily medication"
        assert new_task.recurrence == "daily"
        assert new_task.pet == pet


class TestConflictDetection:
    """Test suite for conflict detection functionality"""
    
    def test_empty_scheduler_no_conflicts(self, scheduler):
        """Empty scheduler should have no conflicts"""
        conflicts = scheduler.detect_conflicts()
        assert conflicts == []
    
    def test_single_task_no_conflict(self, scheduler, task):
        """Single task should not trigger conflicts"""
        scheduler.add_task(task)
        conflicts = scheduler.detect_conflicts()
        assert conflicts == []
    
    def test_completed_task_ignored_in_conflicts(self, scheduler, pet):
        """Completed tasks should be ignored in conflict detection"""
        now = datetime(2026, 3, 31, 14, 0, 0)
        t1 = Task(task_id="t1", task_type=TaskType.FEEDING, pet=pet, due_time=now, priority=2, description="T1", completed=False)
        t2 = Task(task_id="t2", task_type=TaskType.WALK, pet=pet, due_time=now, priority=2, description="T2", completed=True)
        
        scheduler.add_task(t1)
        scheduler.add_task(t2)
        
        # t2 is completed, so no conflict
        conflicts = scheduler.detect_conflicts()
        assert conflicts == []
    
    def test_same_pet_same_time_conflict(self, scheduler, pet):
        """Same pet with multiple tasks at same time should be detected"""
        now = datetime(2026, 3, 31, 15, 30, 0)
        t1 = Task(task_id="t1", task_type=TaskType.WALK, pet=pet, due_time=now, priority=2, description="Walk", completed=False)
        t2 = Task(task_id="t2", task_type=TaskType.GROOMING, pet=pet, due_time=now, priority=2, description="Groom", completed=False)
        
        scheduler.add_task(t1)
        scheduler.add_task(t2)
        
        conflicts = scheduler.detect_conflicts()
        assert len(conflicts) >= 1
        # Should have a message about Buddy having multiple tasks
        assert any("Buddy" in c for c in conflicts)
    
    def test_multiple_pets_same_time_conflict(self, scheduler, owner):
        """Different pets at same time should trigger owner conflict"""
        max_pet = Pet(pet_id="p1", name="Max", species="Dog", breed="Lab", age=3, health_info="Healthy", owner=owner)
        luna_pet = Pet(pet_id="p2", name="Luna", species="Cat", breed="Siamese", age=2, health_info="Healthy", owner=owner)
        
        now = datetime(2026, 3, 31, 15, 30, 0)
        t1 = Task(task_id="t1", task_type=TaskType.WALK, pet=max_pet, due_time=now, priority=2, description="Walk Max", completed=False)
        t2 = Task(task_id="t2", task_type=TaskType.WALK, pet=luna_pet, due_time=now, priority=2, description="Walk Luna", completed=False)
        
        scheduler.add_task(t1)
        scheduler.add_task(t2)
        
        conflicts = scheduler.detect_conflicts()
        assert len(conflicts) >= 1
        # Should have owner conflict message
        assert any("OWNER CONFLICT" in c for c in conflicts)
    
    def test_both_conflict_types_reported(self, scheduler, owner):
        """Both pet conflict and owner conflict should be reported at same time"""
        max_pet = Pet(pet_id="p1", name="Max", species="Dog", breed="Lab", age=3, health_info="Healthy", owner=owner)
        luna_pet = Pet(pet_id="p2", name="Luna", species="Cat", breed="Siamese", age=2, health_info="Healthy", owner=owner)
        
        now = datetime(2026, 3, 31, 15, 30, 0)
        # Two tasks for Max at same time
        t1 = Task(task_id="t1", task_type=TaskType.WALK, pet=max_pet, due_time=now, priority=2, description="Walk", completed=False)
        t2 = Task(task_id="t2", task_type=TaskType.GROOMING, pet=max_pet, due_time=now, priority=2, description="Groom", completed=False)
        # One task for Luna at same time
        t3 = Task(task_id="t3", task_type=TaskType.MEDICATION, pet=luna_pet, due_time=now, priority=1, description="Med", completed=False)
        
        scheduler.add_task(t1)
        scheduler.add_task(t2)
        scheduler.add_task(t3)
        
        conflicts = scheduler.detect_conflicts()
        
        # Should have at least 2 conflicts: pet conflict + owner conflict
        assert len(conflicts) >= 2
        has_pet_conflict = any("Max" in c and "multiple tasks" in c for c in conflicts)
        has_owner_conflict = any("OWNER CONFLICT" in c for c in conflicts)
        assert has_pet_conflict and has_owner_conflict
    
    def test_multiple_time_slots_with_conflicts(self, scheduler, pet, owner):
        """Multiple time slots can each have separate conflicts"""
        pet2 = Pet(pet_id="p2", name="Buddy2", species="Dog", breed="Beagle", age=2, health_info="Healthy", owner=owner)
        
        # First time slot: conflict
        now_1 = datetime(2026, 3, 31, 10, 0, 0)
        t1 = Task(task_id="t1", task_type=TaskType.FEEDING, pet=pet, due_time=now_1, priority=2, description="T1", completed=False)
        t2 = Task(task_id="t2", task_type=TaskType.WALK, pet=pet, due_time=now_1, priority=2, description="T2", completed=False)
        
        # Second time slot: no conflict
        now_2 = datetime(2026, 3, 31, 11, 0, 0)
        t3 = Task(task_id="t3", task_type=TaskType.MEDICATION, pet=pet2, due_time=now_2, priority=1, description="T3", completed=False)
        
        # Third time slot: conflict
        now_3 = datetime(2026, 3, 31, 12, 0, 0)
        t4 = Task(task_id="t4", task_type=TaskType.WALK, pet=pet, due_time=now_3, priority=2, description="T4", completed=False)
        t5 = Task(task_id="t5", task_type=TaskType.WALK, pet=pet2, due_time=now_3, priority=2, description="T5", completed=False)
        
        scheduler.add_task(t1)
        scheduler.add_task(t2)
        scheduler.add_task(t3)
        scheduler.add_task(t4)
        scheduler.add_task(t5)
        
        conflicts = scheduler.detect_conflicts()
        
        # Should detect conflicts in slots 1 and 3, not 2
        assert len(conflicts) >= 2


class TestPetManagement:
    """Tests for pet management and duplicate prevention"""
    
    def test_add_pet_success(self, owner):
        """Successfully add a pet to owner's collection"""
        pet = Pet(
            pet_id="pet_001",
            name="Max",
            species="Dog",
            breed="Golden Retriever",
            age=5,
            health_info="Healthy",
            owner=owner
        )
        
        result = owner.add_pet(pet)
        
        assert result is True
        assert len(owner.pets) == 1
        assert owner.pets[0].name == "Max"
    
    def test_add_duplicate_pet_by_id(self, owner):
        """Cannot add pet with duplicate pet_id"""
        pet1 = Pet(
            pet_id="pet_001",
            name="Max",
            species="Dog",
            breed="Golden Retriever",
            age=5,
            health_info="Healthy",
            owner=owner
        )
        
        pet2 = Pet(
            pet_id="pet_001",  # Same ID
            name="Luna",
            species="Dog",
            breed="Husky",
            age=3,
            health_info="Healthy",
            owner=owner
        )
        
        result1 = owner.add_pet(pet1)
        result2 = owner.add_pet(pet2)
        
        assert result1 is True
        assert result2 is False  # Duplicate ID rejected
        assert len(owner.pets) == 1
    
    def test_add_duplicate_pet_by_name(self, owner):
        """Cannot add pet with duplicate name (case-insensitive)"""
        pet1 = Pet(
            pet_id="pet_001",
            name="Max",
            species="Dog",
            breed="Golden Retriever",
            age=5,
            health_info="Healthy",
            owner=owner
        )
        
        pet2 = Pet(
            pet_id="pet_002",
            name="max",  # Same name, different case
            species="Dog",
            breed="Husky",
            age=3,
            health_info="Healthy",
            owner=owner
        )
        
        result1 = owner.add_pet(pet1)
        result2 = owner.add_pet(pet2)
        
        assert result1 is True
        assert result2 is False  # Duplicate name rejected
        assert len(owner.pets) == 1
    
    def test_add_multiple_different_pets(self, owner):
        """Can add multiple pets with different names"""
        pet1 = Pet(
            pet_id="pet_001",
            name="Max",
            species="Dog",
            breed="Golden Retriever",
            age=5,
            health_info="Healthy",
            owner=owner
        )
        
        pet2 = Pet(
            pet_id="pet_002",
            name="Luna",
            species="Dog",
            breed="Husky",
            age=3,
            health_info="Healthy",
            owner=owner
        )
        
        result1 = owner.add_pet(pet1)
        result2 = owner.add_pet(pet2)
        
        assert result1 is True
        assert result2 is True
        assert len(owner.pets) == 2
        assert owner.pets[0].name == "Max"
        assert owner.pets[1].name == "Luna"
    
    def test_remove_pet_by_id(self, owner):
        """Successfully remove a pet by pet_id"""
        pet1 = Pet(
            pet_id="pet_001",
            name="Max",
            species="Dog",
            breed="Golden Retriever",
            age=5,
            health_info="Healthy",
            owner=owner
        )
        
        pet2 = Pet(
            pet_id="pet_002",
            name="Luna",
            species="Dog",
            breed="Husky",
            age=3,
            health_info="Healthy",
            owner=owner
        )
        
        owner.add_pet(pet1)
        owner.add_pet(pet2)
        assert len(owner.pets) == 2
        
        result = owner.remove_pet("pet_001")
        
        assert result is True
        assert len(owner.pets) == 1
        assert owner.pets[0].name == "Luna"
    
    def test_remove_nonexistent_pet(self, owner):
        """Cannot remove a pet that doesn't exist"""
        result = owner.remove_pet("pet_999")
        
        assert result is False
        assert len(owner.pets) == 0
    
    def test_reuse_name_after_removal(self, owner):
        """Can add pet with same name after removing previous pet"""
        pet1 = Pet(
            pet_id="pet_001",
            name="Max",
            species="Dog",
            breed="Golden Retriever",
            age=5,
            health_info="Healthy",
            owner=owner
        )
        
        pet2 = Pet(
            pet_id="pet_002",
            name="Max",  # Same name
            species="Dog",
            breed="Husky",
            age=3,
            health_info="Healthy",
            owner=owner
        )
        
        result1 = owner.add_pet(pet1)
        assert result1 is True
        
        result2 = owner.add_pet(pet2)
        assert result2 is False  # Can't add duplicate
        
        owner.remove_pet("pet_001")
        result3 = owner.add_pet(pet2)
        assert result3 is True  # Now can add with same name
        assert len(owner.pets) == 1
    
    def test_get_pets(self, owner):
        """Get list of all owner's pets"""
        pet1 = Pet(
            pet_id="pet_001",
            name="Max",
            species="Dog",
            breed="Golden Retriever",
            age=5,
            health_info="Healthy",
            owner=owner
        )
        
        pet2 = Pet(
            pet_id="pet_002",
            name="Luna",
            species="Dog",
            breed="Husky",
            age=3,
            health_info="Healthy",
            owner=owner
        )
        
        owner.add_pet(pet1)
        owner.add_pet(pet2)
        
        pets = owner.get_pets()
        
        assert len(pets) == 2
        assert pets[0].name == "Max"
        assert pets[1].name == "Luna"
