import streamlit as st
import json
from pathlib import Path
from datetime import datetime, timedelta
from pawpal_system import Owner, Pet, Scheduler, Task, TaskType
from ai_agent import CatTaskPlanningAgent, CatProfile


def map_ai_task_to_tasktype(task_type: str) -> TaskType:
    """Map free-form AI task labels to the app's TaskType enum."""
    label = task_type.lower()

    if "feed" in label:
        return TaskType.FEEDING
    if "medication" in label or "injection" in label:
        return TaskType.MEDICATION
    if "groom" in label or "eye" in label or "dental" in label:
        return TaskType.GROOMING
    if "play" in label or "exercise" in label or "training" in label:
        return TaskType.TRAINING
    return TaskType.APPOINTMENT


def recurrence_from_frequency(frequency: str):
    """Infer recurrence from model-provided frequency text."""
    freq = frequency.lower()
    if "daily" in freq or "twice" in freq or "morning" in freq or "evening" in freq:
        return "daily"
    if "weekly" in freq:
        return "weekly"
    return None


def parse_suggested_time(suggested_time: str):
    """Best-effort parsing of suggested text times into a concrete time value."""
    lower = suggested_time.lower()
    if "morning" in lower:
        return datetime.strptime("09:00", "%H:%M").time()
    if "midday" in lower or "noon" in lower:
        return datetime.strptime("12:00", "%H:%M").time()
    if "afternoon" in lower:
        return datetime.strptime("15:00", "%H:%M").time()
    if "evening" in lower or "night" in lower:
        return datetime.strptime("18:00", "%H:%M").time()

    for fmt in ["%H:%M", "%I:%M %p", "%I %p"]:
        try:
            return datetime.strptime(suggested_time.strip(), fmt).time()
        except ValueError:
            continue

    return datetime.strptime("10:00", "%H:%M").time()


def load_breed_options():
    """Load cat breed names from the knowledge base for dropdowns."""
    breeds_file = Path("knowledge_base") / "breeds.json"
    try:
        with open(breeds_file, "r") as f:
            data = json.load(f)
        breeds = data.get("breeds", {})
        return sorted([entry.get("name", key.replace("_", " ").title()) for key, entry in breeds.items()])
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        # Safe fallback so cat creation is never blocked by KB file issues.
        return [
            "Abyssinian",
            "Bengal",
            "Domestic Shorthair",
            "Maine Coon",
            "Persian",
            "Ragdoll",
            "Siamese",
        ]

st.set_page_config(page_title="PawPal+", page_icon="🐱", layout="wide")

st.title("🐱 PawPal+")

st.markdown(
    """
Welcome to PawPal+, your cat care management system.

This app helps you plan and organize your cat's daily routine with intelligent task scheduling.
"""
)

st.divider()

# Initialize session state
if "owner" not in st.session_state:
    st.session_state.owner = None

if "scheduler" not in st.session_state:
    st.session_state.scheduler = None

if "pets" not in st.session_state:
    st.session_state.pets = []

if "pet_counter" not in st.session_state:
    st.session_state.pet_counter = 0

if "ai_agent" not in st.session_state:
    st.session_state.ai_agent = None

if "ai_plan" not in st.session_state:
    st.session_state.ai_plan = None

if "ai_plan_id" not in st.session_state:
    st.session_state.ai_plan_id = 0

if "manual_task_time" not in st.session_state:
    st.session_state.manual_task_time = datetime.now().replace(second=0, microsecond=0).time()

# Owner Setup
st.subheader("👤 Owner Information")
col1, col2, col3, col4 = st.columns(4)

with col1:
    owner_name = st.text_input("Owner name", value="Jordan")
with col2:
    owner_email = st.text_input("Email", value="jordan@example.com")
with col3:
    owner_phone = st.text_input("Phone", value="555-0000")
with col4:
    owner_address = st.text_input("Address", value="123 Main St")

if st.button("Initialize Owner & Scheduler"):
    st.session_state.owner = Owner(
        name=owner_name,
        email=owner_email,
        phone=owner_phone,
        address=owner_address
    )
    st.session_state.scheduler = Scheduler(
        scheduler_id="sched_001",
        owner=st.session_state.owner
    )
    st.success(f"✅ Owner '{owner_name}' and Scheduler initialized!")

if st.session_state.owner:
    st.info(f"Owner: **{st.session_state.owner.name}** | Email: {st.session_state.owner.email}")

st.divider()

# Pet Management
st.subheader("🐈 Manage Cats")

if st.session_state.owner:
    breed_options = load_breed_options()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        pet_name = st.text_input("Cat name", value="Mochi")
    with col2:
        pet_breed = st.selectbox("Breed", options=breed_options, index=0)
    with col3:
        pet_age = st.number_input("Age (years)", min_value=0, max_value=30, value=3)
    
    pet_health = st.text_area("Health info", value="Healthy, up to date on vaccinations")
    
    if st.button("Add Cat"):
        # Check if cat name already exists
        existing_names = [p.name.lower() for p in st.session_state.owner.pets]
        if pet_name.lower() in existing_names:
            st.error(f"❌ A cat named '{pet_name}' already exists! Choose a different name.")
        else:
            # Create new cat with unique ID
            st.session_state.pet_counter += 1
            pet = Pet(
                pet_id=f"pet_{st.session_state.pet_counter:03d}",
                name=pet_name,
                species="Cat",
                breed=pet_breed,
                age=pet_age,
                health_info=pet_health,
                owner=st.session_state.owner
            )
            
            # Use the add_pet() method with duplicate checking
            if st.session_state.owner.add_pet(pet):
                st.session_state.pets = st.session_state.owner.pets
                st.success(f"✅ Cat '{pet_name}' added successfully!")
            else:
                st.error(f"❌ Could not add cat '{pet_name}'. A cat with this ID or name may already exist.")
    
    if st.session_state.pets:
        st.markdown("### Current Cats")
        for pet in st.session_state.pets:
            st.info(f"🐾 **{pet.name}** ({pet.breed}, {pet.age} years) - {pet.health_info}")
else:
    st.warning("⚠️ Please initialize an owner first.")

st.divider()

# AI Planner
st.subheader("🤖 AI Cat Care Planner")

if st.session_state.owner and st.session_state.pets:
    st.caption("Generate an AI task plan using cat profile + retrieved care guidelines.")

    ai_col1, ai_col2 = st.columns(2)

    with ai_col1:
        ai_pet = st.selectbox(
            "Select cat for AI planning",
            options=st.session_state.pets,
            format_func=lambda p: f"{p.name} ({p.breed})",
            key="ai_pet_select",
        )
        ai_conditions = st.text_input(
            "Health conditions (comma-separated)",
            value="",
            help="Example: asthma, chronic kidney disease",
        )

    with ai_col2:
        ai_preferences = st.text_area(
            "Owner preferences (optional)",
            value="Keep routines simple, prioritize evenings",
            help="Example: avoid mornings, short play sessions, strict medication times",
        )

    if st.button("Generate AI Plan"):
        try:
            if st.session_state.ai_agent is None:
                st.session_state.ai_agent = CatTaskPlanningAgent()

            condition_list = [c.strip() for c in ai_conditions.split(",") if c.strip()]
            preference_list = [p.strip() for p in ai_preferences.split(",") if p.strip()]

            profile = CatProfile(
                name=ai_pet.name,
                breed=ai_pet.breed,
                age_years=int(ai_pet.age),
                health_conditions=condition_list,
                preferences=preference_list,
            )

            st.session_state.ai_plan = st.session_state.ai_agent.create_plan(profile)
            st.session_state.ai_plan_id += 1
            st.success("✅ AI plan generated successfully.")
        except Exception as e:
            st.error(f"❌ Could not generate AI plan: {e}")

    if st.session_state.ai_plan:
        plan_response = st.session_state.ai_plan
        plan = plan_response.get("plan", {})
        suggested_tasks = plan.get("suggested_tasks", [])
        validation = plan_response.get("validation", {})

        source = plan_response.get("source", "unknown")
        st.markdown(f"**Model Source:** `{source}`")
        st.markdown(f"**Plan Summary:** {plan.get('summary', 'No summary provided.')} ")

        if validation:
            val_col1, val_col2, val_col3 = st.columns(3)
            with val_col1:
                st.metric("Validation Score", validation.get("score", 0.0))
            with val_col2:
                st.metric("Validation Passed", "Yes" if validation.get("passed") else "No")
            with val_col3:
                st.metric("Suggested Tasks", len(suggested_tasks))

            for err in validation.get("errors", []):
                st.error(f"Validation error: {err}")
            for warn in validation.get("warnings", []):
                st.warning(f"Validation warning: {warn}")

        if suggested_tasks:
            st.markdown("### Suggested AI Tasks")
            task_rows = []
            for task in suggested_tasks:
                task_rows.append(
                    {
                        "Type": task.get("task_type", ""),
                        "Priority": task.get("priority", 0),
                        "Frequency": task.get("frequency", ""),
                        "Suggested Time": task.get("suggested_time", ""),
                        "Confidence": task.get("confidence", 0.0),
                        "Description": task.get("description", ""),
                    }
                )
            st.table(task_rows)
            st.markdown("#### Select Tasks to Add")
            selected_tasks = []
            for idx, task in enumerate(suggested_tasks):
                checkbox_key = f"ai_task_select_{st.session_state.ai_plan_id}_{idx}"
                label = (
                    f"{task.get('task_type', 'Task')} | "
                    f"{task.get('suggested_time', 'Flexible')} | "
                    f"P{task.get('priority', 3)}"
                )
                if st.checkbox(label, value=True, key=checkbox_key):
                    selected_tasks.append((idx, task))

            if st.button("Add Selected AI Tasks"):
                if not selected_tasks:
                    st.warning("Please select at least one AI task to add.")
                else:
                    added = 0
                    now = datetime.now()
                    for idx, task in selected_tasks:
                        due_time = parse_suggested_time(task.get("suggested_time", ""))
                        due_datetime = datetime.combine(now.date(), due_time) + timedelta(minutes=idx * 15)

                        new_task = Task(
                            task_id=st.session_state.scheduler.generate_task_id(),
                            task_type=map_ai_task_to_tasktype(task.get("task_type", "appointment")),
                            pet=ai_pet,
                            due_time=due_datetime,
                            priority=max(1, min(5, int(task.get("priority", 3)))),
                            description=task.get("description", "AI-generated cat care task"),
                            completed=False,
                            recurrence=recurrence_from_frequency(task.get("frequency", "")),
                        )
                        st.session_state.scheduler.add_task(new_task)
                        added += 1

                    st.success(f"✅ Added {added} selected AI task(s) to the schedule.")
                    st.rerun()
else:
    st.info("Initialize owner and add at least one cat to use AI planning.")

st.divider()

# Task Scheduling
st.subheader("📋 Schedule Tasks")

if st.session_state.owner and st.session_state.pets:
    st.markdown("### Add a Task")
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_pet = st.selectbox(
            "Select cat",
            options=st.session_state.pets,
            format_func=lambda p: f"{p.name} ({p.breed})"
        )
        task_type = st.selectbox(
            "Task type",
            options=[t.value for t in TaskType],
            format_func=lambda x: x.upper()
        )
        task_description = st.text_input("Task description", value="Feed cat")
    
    with col2:
        task_time = st.time_input(
            "Time",
            value=st.session_state.manual_task_time,
            key="manual_task_time",
        )
        task_priority = st.slider("Priority (1=Low, 5=High)", min_value=1, max_value=5, value=3)
    
    if st.button("Schedule Task"):
        due_datetime = datetime.combine(datetime.now().date(), task_time)

        task = Task(
            task_id=st.session_state.scheduler.generate_task_id(),
            task_type=TaskType(task_type),
            pet=selected_pet,
            due_time=due_datetime,
            priority=task_priority,
            description=task_description,
            completed=False
        )
        
        st.session_state.scheduler.add_task(task)
        st.success(f"✅ Task '{task_description}' scheduled for {selected_pet.name} at {task_time}!")
    
    if st.session_state.scheduler.tasks:
        st.markdown("### 📅 Current Schedule (Chronological Order)")
        
        # Use Scheduler.sort_by_time() method
        sorted_tasks = st.session_state.scheduler.sort_by_time()
        
        # Display as table
        task_data = []
        for task in sorted_tasks:
            task_data.append({
                "Status": "✅ Done" if task.completed else "⏳ Pending",
                "Time": task.due_time.strftime('%H:%M'),
                "Cat": task.pet.name,
                "Type": task.task_type.value.capitalize(),
                "Description": task.description,
                "Priority": "⭐" * task.priority
            })
        
        st.table(task_data)
        
        # Conflict Detection Section
        st.markdown("### ⚠️ Schedule Conflicts")
        conflicts = st.session_state.scheduler.detect_conflicts()
        
        if conflicts:
            for conflict in conflicts:
                st.warning(conflict)
        else:
            st.success("✅ No scheduling conflicts detected!")
        
        st.divider()
        
        # Task Filtering Section
        st.markdown("### 🔍 Filter Tasks")
        
        col1, col2 = st.columns(2)
        
        with col1:
            filter_pet = st.selectbox(
                "Filter by Cat (select 'All' to show all)",
                options=["All"] + [p.name for p in st.session_state.pets],
                key="filter_pet_select"
            )
        
        with col2:
            filter_status = st.selectbox(
                "Filter by Status",
                options=["All", "Pending", "Completed"],
                key="filter_status_select"
            )
        
        # Apply filters using Scheduler.filter_tasks() to keep results time-sorted.
        pet_filter = None if filter_pet == "All" else filter_pet
        status_filter = None
        if filter_status == "Pending":
            status_filter = False
        elif filter_status == "Completed":
            status_filter = True

        filtered_tasks = st.session_state.scheduler.filter_tasks(
            pet_name=pet_filter,
            completed=status_filter,
        )
        
        if filtered_tasks:
            st.markdown(f"**Found {len(filtered_tasks)} task(s)**")
            
            for idx, task in enumerate(filtered_tasks):
                with st.expander(
                    f"{'✅' if task.completed else '⏳'} {task.pet.name} - {task.task_type.value.upper()} at {task.due_time.strftime('%H:%M')}"
                ):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**Description:** {task.description}")
                        st.write(f"**Due:** {task.due_time.strftime('%Y-%m-%d %H:%M')}")
                    
                    with col2:
                        st.write(f"**Priority:** {'⭐' * task.priority}")
                        st.write(f"**Status:** {'✅ Completed' if task.completed else '⏳ Pending'}")
                        st.caption(f"Task ID: {task.task_id}")
                    
                    with col3:
                        if not task.completed:
                            if st.button("✓ Mark Complete", key=f"complete_{task.task_id}"):
                                task.mark_complete(st.session_state.scheduler)
                                st.success(f"Task marked complete! {'📌 Next occurrence created.' if task.recurrence else ''}")
                                st.rerun()

                            with st.form(key=f"reschedule_form_{task.task_id}_{idx}"):
                                new_task_time = st.time_input(
                                    "New time",
                                    value=task.due_time.time(),
                                    key=f"resched_time_{task.task_id}_{idx}",
                                )
                                reschedule_submitted = st.form_submit_button("🕒 Reschedule")

                            if reschedule_submitted:
                                requested_time = datetime.combine(task.due_time.date(), new_task_time)
                                old_time = task.due_time
                                try:
                                    st.session_state.scheduler.reschedule_task(task.task_id, requested_time)
                                    updated_task = next(
                                        (t for t in st.session_state.scheduler.tasks if t.task_id == task.task_id),
                                        None,
                                    )
                                    final_time = updated_task.due_time if updated_task else requested_time
                                    if final_time != requested_time:
                                        st.warning(
                                            f"Conflict at {requested_time.strftime('%H:%M')}. "
                                            f"Moved to {final_time.strftime('%H:%M')}"
                                        )
                                    else:
                                        st.success(
                                            f"Task rescheduled from {old_time.strftime('%H:%M')} to {final_time.strftime('%H:%M')}"
                                        )
                                except ValueError as exc:
                                    st.error(f"Could not reschedule task: {exc}")
                                except RuntimeError as exc:
                                    st.error(f"Could not find an available time: {exc}")
                                st.rerun()

                        if st.button("🗑 Remove Task", key=f"remove_{task.task_id}_{idx}"):
                            removed = st.session_state.scheduler.remove_task(task.task_id)
                            if removed:
                                st.success(f"Task {task.task_id} removed.")
                            else:
                                st.warning(f"Task {task.task_id} was not found.")
                            st.rerun()
        else:
            st.info("No tasks match your filters.")
        
        st.divider()
        
        # Task Summary Section
        st.markdown("### 📊 Task Summary")
        
        summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
        
        pending_count = len([t for t in st.session_state.scheduler.tasks if not t.completed])
        completed_count = len([t for t in st.session_state.scheduler.tasks if t.completed])
        recurring_count = len([t for t in st.session_state.scheduler.tasks if t.recurrence])
        
        with summary_col1:
            st.metric("Total Tasks", len(st.session_state.scheduler.tasks))
        with summary_col2:
            st.metric("Pending", pending_count)
        with summary_col3:
            st.metric("Completed", completed_count)
        with summary_col4:
            st.metric("Recurring", recurring_count)

    else:
        st.info("No tasks scheduled yet. Add one above.")

elif st.session_state.owner:
    st.warning("⚠️ Please add at least one cat before scheduling tasks.")

else:
    st.warning("⚠️ Please initialize an owner first.")
