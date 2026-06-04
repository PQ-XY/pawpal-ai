"""
Knowledge Retriever for PawPal+ Cat Care System

This module implements the RAG (Retrieval-Augmented Generation) component.
It loads and retrieves cat care guidelines from the knowledge base JSON files
based on breed, age group, and health conditions.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class KnowledgeRetriever:
    """Retrieves cat care guidelines from the knowledge base."""
    
    def __init__(self, knowledge_base_path: str = "knowledge_base"):
        """
        Initialize the Knowledge Retriever.
        
        Args:
            knowledge_base_path: Path to the knowledge base directory
        """
        self.kb_path = Path(knowledge_base_path)
        self.breeds: Dict = {}
        self.health_conditions: Dict = {}
        self.age_groups: Dict = {}
        self.task_templates: Dict = {}
        
        # Load all knowledge base files
        self._load_knowledge_base()
        logger.info("Knowledge Retriever initialized successfully")
    
    def _load_knowledge_base(self) -> None:
        """Load all JSON files from the knowledge base directory."""
        try:
            # Load breeds
            breeds_path = self.kb_path / "breeds.json"
            if breeds_path.exists():
                with open(breeds_path, 'r') as f:
                    data = json.load(f)
                    self.breeds = data.get('breeds', {})
                logger.info(f"Loaded {len(self.breeds)} cat breeds")
            
            # Load health conditions
            health_path = self.kb_path / "health_conditions.json"
            if health_path.exists():
                with open(health_path, 'r') as f:
                    data = json.load(f)
                    self.health_conditions = data.get('health_conditions', {})
                logger.info(f"Loaded {len(self.health_conditions)} health conditions")
            
            # Load age groups
            age_path = self.kb_path / "age_groups.json"
            if age_path.exists():
                with open(age_path, 'r') as f:
                    data = json.load(f)
                    self.age_groups = data.get('age_groups', {})
                logger.info(f"Loaded {len(self.age_groups)} age groups")
            
            # Load task templates
            tasks_path = self.kb_path / "task_templates.json"
            if tasks_path.exists():
                with open(tasks_path, 'r') as f:
                    data = json.load(f)
                    self.task_templates = data.get('task_templates', {})
                logger.info(f"Loaded {len(self.task_templates)} task templates")
        
        except Exception as e:
            logger.error(f"Error loading knowledge base: {e}")
            raise
    
    def get_breed_info(self, breed: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve information about a specific cat breed.
        
        Args:
            breed: Breed name (case-insensitive)
        
        Returns:
            Breed information dict or None if not found
        """
        breed_lower = breed.lower().replace(" ", "_")
        
        if breed_lower in self.breeds:
            logger.info(f"Retrieved info for breed: {breed}")
            return self.breeds[breed_lower]
        
        logger.warning(f"Breed not found: {breed}")
        return None
    
    def get_age_group_info(self, age_group: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve information about a specific age group.
        
        Args:
            age_group: Age group name (kitten, adult, senior) - case-insensitive
        
        Returns:
            Age group information dict or None if not found
        """
        age_lower = age_group.lower()
        
        if age_lower in self.age_groups:
            logger.info(f"Retrieved info for age group: {age_group}")
            return self.age_groups[age_lower]
        
        logger.warning(f"Age group not found: {age_group}")
        return None
    
    def infer_age_group(self, age_years: int) -> str:
        """
        Infer age group based on cat's age in years.
        
        Args:
            age_years: Cat's age in years
        
        Returns:
            Age group name (kitten, adult, or senior)
        """
        if age_years < 1:
            return "kitten"
        elif age_years < 7:
            return "adult"
        else:
            return "senior"
    
    def get_health_condition_info(self, condition: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve information about a specific health condition.
        
        Args:
            condition: Health condition name - case-insensitive
        
        Returns:
            Health condition information dict or None if not found
        """
        condition_lower = condition.lower().replace(" ", "_")
        
        if condition_lower in self.health_conditions:
            logger.info(f"Retrieved info for condition: {condition}")
            return self.health_conditions[condition_lower]
        
        logger.warning(f"Health condition not found: {condition}")
        return None
    
    def get_task_template(self, task_type: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a task template by type.
        
        Args:
            task_type: Task type name (e.g., feeding, grooming, medication)
        
        Returns:
            Task template dict or None if not found
        """
        task_lower = task_type.lower().replace(" ", "_")
        
        if task_lower in self.task_templates:
            logger.info(f"Retrieved task template: {task_type}")
            return self.task_templates[task_lower]
        
        logger.warning(f"Task template not found: {task_type}")
        return None
    
    def retrieve_for_cat(
        self,
        breed: str,
        age_years: int,
        health_conditions: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Retrieve all relevant knowledge for a specific cat.
        
        This is the main RAG retrieval function that combines:
        - Breed-specific guidelines
        - Age-appropriate care
        - Health condition requirements
        - Relevant task templates
        
        Args:
            breed: Cat's breed
            age_years: Cat's age in years
            health_conditions: List of health conditions (optional)
        
        Returns:
            Dictionary with retrieved knowledge organized by category
        """
        logger.info(f"Retrieving knowledge for cat: {breed}, age {age_years}, conditions: {health_conditions}")
        
        retrieved_knowledge = {
            "breed_info": None,
            "age_info": None,
            "health_conditions": [],
            "recommended_tasks": set(),
            "health_priorities": [],
            "key_guidelines": []
        }
        
        # Get breed info
        breed_info = self.get_breed_info(breed)
        if breed_info:
            retrieved_knowledge["breed_info"] = breed_info
            logger.info(f"Added breed info: {breed}")
        
        # Get age group info
        age_group = self.infer_age_group(age_years)
        age_info = self.get_age_group_info(age_group)
        if age_info:
            retrieved_knowledge["age_info"] = age_info
            logger.info(f"Inferred age group: {age_group}")
        
        # Get health condition info
        if health_conditions:
            for condition in health_conditions:
                condition_info = self.get_health_condition_info(condition)
                if condition_info:
                    retrieved_knowledge["health_conditions"].append(condition_info)
                    
                    # Add health-specific tasks to recommendations
                    if "recommended_tasks" in condition_info:
                        retrieved_knowledge["recommended_tasks"].update(
                            condition_info["recommended_tasks"]
                        )
                    
                    # Track health priorities
                    if "severity" in condition_info:
                        retrieved_knowledge["health_priorities"].append({
                            "condition": condition,
                            "severity": condition_info["severity"],
                            "care_requirements": condition_info.get("care_requirements", [])
                        })
                    logger.info(f"Added health condition: {condition}")
        
        # Collect recommended tasks from all sources
        if breed_info and "recommended_tasks" in breed_info:
            retrieved_knowledge["recommended_tasks"].update(breed_info["recommended_tasks"])
        
        if age_info and "recommended_tasks" in age_info:
            retrieved_knowledge["recommended_tasks"].update(age_info["recommended_tasks"])
        
        # Generate key guidelines summary
        guidelines = []
        
        if breed_info:
            guidelines.append(f"Breed: {breed_info.get('name', breed)}")
            if "special_care" in breed_info:
                guidelines.extend(breed_info["special_care"])
        
        if age_info:
            guidelines.append(f"Age group: {age_info.get('name', age_group)}")
            if "key_characteristics" in age_info:
                guidelines.extend(age_info["key_characteristics"])
        
        for condition in retrieved_knowledge["health_conditions"]:
            guidelines.append(f"Condition: {condition.get('name', 'unknown')}")
            if "care_requirements" in condition:
                guidelines.extend(condition["care_requirements"][:2])  # First 2 requirements
        
        retrieved_knowledge["key_guidelines"] = guidelines
        
        # Convert set to list for JSON serialization
        retrieved_knowledge["recommended_tasks"] = list(retrieved_knowledge["recommended_tasks"])
        
        logger.info(f"Retrieved knowledge with {len(retrieved_knowledge['recommended_tasks'])} recommended tasks")
        return retrieved_knowledge
    
    def get_task_frequency_recommendations(
        self,
        breed: str,
        age_years: int,
        health_conditions: Optional[List[str]] = None
    ) -> Dict[str, str]:
        """
        Get recommended task frequencies for a cat based on profile.
        
        Args:
            breed: Cat's breed
            age_years: Cat's age in years
            health_conditions: List of health conditions
        
        Returns:
            Dictionary mapping task types to recommended frequencies
        """
        age_group = self.infer_age_group(age_years)
        recommendations = {}
        
        # Get age-specific frequencies
        age_info = self.get_age_group_info(age_group)
        
        for task_type, template in self.task_templates.items():
            if age_group in template.get("frequency_suggestions", {}):
                recommendations[task_type] = template["frequency_suggestions"][age_group]
        
        # Override with health condition frequencies if applicable
        if health_conditions:
            for condition in health_conditions:
                condition_info = self.get_health_condition_info(condition)
                if condition_info and "task_frequency" in condition_info:
                    # Health conditions take priority
                    condition_freq = condition_info["task_frequency"]
                    recommended_tasks = condition_info.get("recommended_tasks", [])
                    for task in recommended_tasks:
                        recommendations[task] = condition_freq
        
        logger.info(f"Generated task frequency recommendations: {len(recommendations)} tasks")
        return recommendations


# Example usage for testing
if __name__ == "__main__":
    # Initialize retriever
    retriever = KnowledgeRetriever()
    
    # Example 1: Retrieve knowledge for a healthy adult Maine Coon
    print("\n=== Example 1: Adult Maine Coon ===")
    knowledge = retriever.retrieve_for_cat(
        breed="Maine Coon",
        age_years=3
    )
    print(f"Recommended tasks: {knowledge['recommended_tasks']}")
    print(f"Key guidelines: {knowledge['key_guidelines'][:3]}")
    
    # Example 2: Senior Siamese with chronic kidney disease
    print("\n=== Example 2: Senior Siamese with CKD ===")
    knowledge = retriever.retrieve_for_cat(
        breed="Siamese",
        age_years=10,
        health_conditions=["Chronic Kidney Disease"]
    )
    print(f"Recommended tasks: {knowledge['recommended_tasks']}")
    print(f"Health priorities: {knowledge['health_priorities']}")
    
    # Example 3: Get task frequencies
    print("\n=== Example 3: Task Frequencies ===")
    frequencies = retriever.get_task_frequency_recommendations(
        breed="Bengal",
        age_years=2
    )
    for task, freq in list(frequencies.items())[:5]:
        print(f"  {task}: {freq}")
