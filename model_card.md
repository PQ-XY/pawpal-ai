## What are the limitations or biases in your system?
    We only focus on Cat to narraow down the objects and only provide some typical cases in knowledge base to control the data size. 

## Could your AI be misused, and how would you prevent that?
    In our case, AI cannot be misused since all the prompt we send to the AI model is beckend controled. User provide selection input based on pet's info and we retrive the additional info from our RAG and send it along with the pet profile to AI to generate plans. So user are not directly connected with AI mode. 

## What surprised you while testing your AI's reliability?
    Even we include the info from our knowledge base, sometimes, the result came back from AI missed the main points from the knowledge base. 

## describe your collaboration with AI during this project. Identify one instance when the AI gave a helpful suggestion and one instance where its suggestion was flawed or incorrect.
    At the beginning of the project, AI and I brainstorm the features and AI inhencement together and made the direction together. Then We broke it into steps and we built the project together step by step. At end of each step, we test the step is working and then move to the next one rather than trying to finish all and doing testing. 

    When we tried to implement the remove_tasks(), AI didn't get it through at first time. After AI implement it, I checked that when I hit the "Remove" button, nothing happened. I explian the situation and ask it to check mark_complet() function first and follow the logic. Then it could get it right. 

    AI is helpful overall in the process. It show you how to implememnt functions you never did before like RAG and validator. It help you to test and connect different components together. 
