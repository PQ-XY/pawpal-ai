from datetime import datetime, timedelta
from pawpal_system import Owner, Pet, Scheduler, Task, TaskType


def print_todays_schedule(scheduler: Scheduler) -> None:
    """Print today's scheduled tasks in chronological order"""
    today = datetime.now().date()
    
    # Filter tasks for today
    todays_tasks = [
        task for task in scheduler.tasks
        if task.due_time.date() == today
    ]
    
    # Sort by due time
    todays_tasks.sort(key=lambda t: t.due_time)
    
    print("\n" + "=" * 60)
    print(f"TODAY'S SCHEDULE - {today.strftime('%A, %B %d, %Y')}")
    print("=" * 60)
    
    if not todays_tasks:
        print("No tasks scheduled for today.")
    else:
        for task in todays_tasks:
            status = "✓" if task.completed else "○"
            time_str = task.due_time.strftime('%H:%M')
            print(f"\n{status} {time_str} - {task.task_type.value.upper()}")
            print(f"   Pet: {task.pet.name}")
            print(f"   {task.description}")
            print(f"   Priority: {'*' * task.priority}")
    
    print("=" * 60)


def demo_conflict_detection():
    """Simplified demo showing conflict detection"""
    print("\n" + "=" * 70)
    print("CONFLICT DETECTION DEMO - Two Tasks at Same Time")
    print("=" * 70)
    
    # Create minimal example with just two pets and a conflict
    owner = Owner(
        name="Test Owner",
        email="test@example.com",
        phone="555-1234",
        address="Test Address"
    )
    
    dog = Pet(
        pet_id="pet_dog",
        name="Buddy",
        species="Dog",
        breed="Beagle",
        age=2,
        health_info="Healthy",
        owner=owner
    )
    
    cat = Pet(
        pet_id="pet_cat",
        name="Whiskers",
        species="Cat",
        breed="Persian",
        age=4,
        health_info="Healthy",
        owner=owner
    )
    
    owner.pets.extend([dog, cat])
    
    # Create scheduler
    scheduler = Scheduler(scheduler_id="demo_sched", owner=owner)
    
    # Create two tasks at EXACTLY the same time
    now = datetime.now()
    conflict_time = now.replace(hour=14, minute=0)
    
    task_a = Task(
        task_id="demo_001",
        task_type=TaskType.WALK,
        pet=dog,
        due_time=conflict_time,
        priority=2,
        description="Walk Buddy in the park",
        completed=False
    )
    
    task_b = Task(
        task_id="demo_002",
        task_type=TaskType.WALK,
        pet=cat,
        due_time=conflict_time,  # SAME TIME!
        priority=2,
        description="Walk Whiskers around the block",
        completed=False
    )
    
    # Add both tasks to scheduler
    scheduler.add_task(task_a)
    scheduler.add_task(task_b)
    
    print(f"\n✓ Added 2 tasks at the same time:")
    print(f"  • {task_a.pet.name}: {task_a.description} @ {conflict_time.strftime('%H:%M')}")
    print(f"  • {task_b.pet.name}: {task_b.description} @ {conflict_time.strftime('%H:%M')}")
    
    # Run conflict detection
    print(f"\nRunning conflict detection...")
    conflicts = scheduler.detect_conflicts()
    
    print(f"\n📋 Result: Found {len(conflicts)} conflict(s)")
    if conflicts:
        for warning in conflicts:
            print(f"\n  {warning}")
    else:
        print("  No conflicts detected")
    
    print("\n" + "=" * 70)


def main():
    """Main function to demonstrate PawPal+ system with an Owner and Pets"""
    
    # Run simple conflict detection demo first
    demo_conflict_detection()
    owner = Owner(
        name="Sarah Chen",
        email="sarah.chen@email.com",
        phone="555-0123",
        address="123 Oak Street, Portland, OR 97201"
    )
    
    # Create the first Pet - a dog
    dog = Pet(
        pet_id="pet_001",
        name="Max",
        species="Dog",
        breed="Golden Retriever",
        age=5,
        health_info="Healthy, up to date on vaccinations. Slight arthritis in rear left leg.",
        owner=owner
    )
    
    # Create the second Pet - a cat
    cat = Pet(
        pet_id="pet_002",
        name="Luna",
        species="Cat",
        breed="Siamese",
        age=3,
        health_info="Healthy. Prone to hairballs.",
        owner=owner
    )
    
    # Add pets to the owner
    owner.pets.append(dog)
    owner.pets.append(cat)
    
    # Create a Scheduler for the owner
    owner.scheduler = Scheduler(scheduler_id="sched_001", owner=owner)
    
    # Create Tasks with different times - ADD OUT OF ORDER
    now = datetime.now()
    
    # Task 3: Luna's Medication (Evening) - ADDED FIRST - RECURRING DAILY
    task_3 = Task(
        task_id="task_003",
        task_type=TaskType.MEDICATION,
        pet=cat,
        due_time=now.replace(hour=20, minute=0),
        priority=1,
        description="Give Luna her daily thyroid medication with food",
        completed=False,
        recurrence="daily"
    )
    
    # Task 1: Feed Max (Morning) - ADDED SECOND - RECURRING DAILY
    task_1 = Task(
        task_id="task_001",
        task_type=TaskType.FEEDING,
        pet=dog,
        due_time=now.replace(hour=8, minute=0),
        priority=3,
        description="Feed Max his morning kibble (2 cups)",
        completed=False,
        recurrence="daily"
    )
    
    # Task 2: Walk Max (Afternoon) - ADDED THIRD
    task_2 = Task(
        task_id="task_002",
        task_type=TaskType.WALK,
        pet=dog,
        due_time=now.replace(hour=15, minute=30),
        priority=2,
        description="Walk Max around the park (30-45 minutes)",
        completed=False
    )
    
    # Task 4: Feed Luna (Morning) - NEW
    task_4 = Task(
        task_id="task_004",
        task_type=TaskType.FEEDING,
        pet=cat,
        due_time=now.replace(hour=8, minute=30),
        priority=3,
        description="Feed Luna her wet food",
        completed=True
    )
    
    # Task 5: CONFLICT TEST - Max groom (same time as walk)
    task_5 = Task(
        task_id="task_005",
        task_type=TaskType.GROOMING,
        pet=dog,
        due_time=now.replace(hour=15, minute=30),
        priority=2,
        description="Groom Max (same time as walk - CONFLICT!)",
        completed=False
    )
    
    # Task 6: CONFLICT TEST - Luna walk (same time as other pet walk)
    task_6 = Task(
        task_id="task_006",
        task_type=TaskType.WALK,
        pet=cat,
        due_time=now.replace(hour=15, minute=30),
        priority=2,
        description="Walk Luna (owner conflict - same time as Max walk)",
        completed=False
    )
    
    # Add tasks to the scheduler OUT OF ORDER
    owner.scheduler.tasks.extend([task_3, task_1, task_2, task_4, task_5, task_6])
    
    # Display owner and pets information
    print(f"Owner: {owner.name}")
    print(f"Email: {owner.email}")
    print(f"Phone: {owner.phone}")
    print(f"Address: {owner.address}")
    print(f"\nPets ({len(owner.pets)}):")
    
    for pet in owner.pets:
        print(f"  - {pet.name} ({pet.species}, {pet.breed}, {pet.age} years old)")
        print(f"    Health: {pet.health_info}")
    
    print(f"\nScheduler ID: {owner.scheduler.scheduler_id}")
    print(f"Active Tasks: {len(owner.scheduler.tasks)}")
    print(f"Completed Tasks: {len(owner.scheduler.completed_tasks)}")
    
    # DEMONSTRATE: Sort by Time
    print("\n" + "=" * 60)
    print("TASKS SORTED BY TIME (Chronological Order)")
    print("=" * 60)
    sorted_tasks = owner.scheduler.sort_by_time()
    for task in sorted_tasks:
        status = "✓" if task.completed else "○"
        time_str = task.due_time.strftime('%H:%M')
        print(f"{status} {time_str} - {task.pet.name}: {task.description}")
    
    # DEMONSTRATE: Filter by Pet Name (Max)
    print("\n" + "=" * 60)
    print("TASKS FOR PET: Max")
    print("=" * 60)
    max_tasks = owner.scheduler.filter_tasks(pet_name="Max")
    for task in max_tasks:
        status = "✓" if task.completed else "○"
        time_str = task.due_time.strftime('%H:%M')
        print(f"{status} {time_str} - {task.task_type.value}: {task.description}")
    
    # DEMONSTRATE: Filter by Pet Name (Luna)
    print("\n" + "=" * 60)
    print("TASKS FOR PET: Luna")
    print("=" * 60)
    luna_tasks = owner.scheduler.filter_tasks(pet_name="Luna")
    for task in luna_tasks:
        status = "✓" if task.completed else "○"
        time_str = task.due_time.strftime('%H:%M')
        print(f"{status} {time_str} - {task.task_type.value}: {task.description}")
    
    # DEMONSTRATE: Filter by Completion Status (Incomplete)
    print("\n" + "=" * 60)
    print("INCOMPLETE TASKS")
    print("=" * 60)
    incomplete_tasks = owner.scheduler.filter_tasks(completed=False)
    for task in incomplete_tasks:
        time_str = task.due_time.strftime('%H:%M')
        print(f"○ {time_str} - {task.pet.name}: {task.description}")
    
    # DEMONSTRATE: Filter by Completion Status (Completed)
    print("\n" + "=" * 60)
    print("COMPLETED TASKS")
    print("=" * 60)
    completed_tasks = owner.scheduler.filter_tasks(completed=True)
    for task in completed_tasks:
        time_str = task.due_time.strftime('%H:%M')
        print(f"✓ {time_str} - {task.pet.name}: {task.description}")
    
    # DEMONSTRATE: Combined Filter (Max's incomplete tasks)
    print("\n" + "=" * 60)
    print("INCOMPLETE TASKS FOR MAX")
    print("=" * 60)
    max_incomplete = owner.scheduler.filter_tasks(pet_name="Max", completed=False)
    for task in max_incomplete:
        time_str = task.due_time.strftime('%H:%M')
        print(f"○ {time_str} - {task.task_type.value}: {task.description}")
    
    # DEMONSTRATE: Recurring Tasks
    print("\n" + "=" * 60)
    print("RECURRING TASKS DEMO")
    print("=" * 60)
    print(f"Total tasks before marking recurring task complete: {len(owner.scheduler.tasks)}")
    
    # Find task_1 (Max's morning feeding - recurring daily)
    max_feeding = owner.scheduler.filter_tasks(pet_name="Max", completed=False)[0]
    print(f"\nMarking '{max_feeding.description}' as complete...")
    print(f"Task recurrence: {max_feeding.recurrence}")
    
    # Mark the recurring task as complete (this should create a new task for tomorrow)
    max_feeding.mark_complete(owner.scheduler)
    
    print(f"Total tasks after marking recurring task complete: {len(owner.scheduler.tasks)}")
    
    # Show all tasks sorted by time (now including the new recurring occurrence)
    print("\nAll tasks after recurring task was completed:")
    all_sorted = owner.scheduler.sort_by_time()
    for task in all_sorted:
        status = "✓" if task.completed else "○"
        time_str = task.due_time.strftime('%Y-%m-%d %H:%M')
        print(f"{status} {time_str} - {task.pet.name}: {task.description}")
    
    # DEMONSTRATE: Conflict Detection
    print("\n" + "=" * 60)
    print("CONFLICT DETECTION")
    print("=" * 60)
    conflicts = owner.scheduler.detect_conflicts()
    if conflicts:
        print(f"Found {len(conflicts)} scheduling conflict(s):\n")
        for warning in conflicts:
            print(warning)
    else:
        print("✓ No scheduling conflicts detected!")
    
    # Print today's schedule
    print_todays_schedule(owner.scheduler)



if __name__ == "__main__":
    main()

