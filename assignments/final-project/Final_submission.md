# 🚀 ECE 464: Databases – Final Capstone
## From Idea to Production: Building Scalable Software in the Agentic Age

The MVP phase is behind us, and it is time to bring your capstone projects across the finish line. The goal remains the same: proving you can take an idea, leverage a modern tech stack, and launch a scalable, production-ready application that is both legitimate and functional.

---

### **Final Deliverables**
Please ensure all of the following are clearly linked in a central document and/or the root `README.md` of your final GitHub repository:

* **GitHub Repository:** The complete source code, README, and full migration/code history.
* **Live Application Link:** A hosted, functional version of your app. This must be accessible via a public URL during final presentations and remain live until grades are finalized.
* **Demo Video:** A ~3-minute walkthrough of your application's core functionality.
* **Local Development Instructions** A readme file containing how to run your project locally.
* **Final Write-up:** A formal document detailing your architecture, schema, and development journey.
* **Final Presentation:** A 10-minute live presentation and Q&A session.

---

### **Core Project & Code Expectations**
To meet the graduate-level standard for ECE 464, your final submission must satisfy these infrastructure and production requirements:

* **Database Schema & Integrity:** I will be looking closely at your database design (targeting **10 to 15 tables**), relational integrity, and how you have indexed your tables to support your specific queries.
* **Database Migrations:** Manual SQL "fixes" or state-changes are not permitted. Your repository must demonstrate the use of a formal migration system (e.g., **Alembic**).
* **Authentication & Data Ownership:** Your application must implement a full user account system with secure login (e.g., **Supabase Auth**) that ensures strict data ownership and access control.
* **Cloud Deployment (Hosting):** Your application must be fully hosted in the cloud (e.g., **Railway** for the backend, **Vercel** for the frontend) and accessible to the public. Localhost-only projects will not be accepted.
* **External Service Integration:** You must successfully integrate at least one major third-party software service via API (e.g., **Stripe** for payments, **Twilio** for SMS, **Square**, etc.).
* **The Complexity Component:** The "non-obvious" technical challenge discussed in your 1-on-1 (e.g., Vector search, complex concurrency, or heavy background jobs) must be fully realized.
* **The Frontend:** While the UI may be "vibecoded," it must be functional enough to demonstrate the underlying backend architecture and data flows seamlessly.

---

### **The Final Write-up**
Create a clean document in your repository covering:

1.  **Mission:** The problem your project solves.
2.  **Schema:** Core tables and relationships (link to your schema definitions).
3.  **Architecture:** High-level view of how your servers, clients, databases, and third-party integrations connect. How did you load your database's state, if you pulled in external data?
4.  **Key Queries:** Highlight 2-3 interesting SQL/ORM queries and explain your indexing strategy for them.
5.  **Complexity Component:** Deep dive into the most technically unique part of your solution.
6.  **The Journey:** A retrospective on roadblocks, what was easier/harder than expected, and your experience with AI-assisted development.
7.  **Scaling:** A brief analysis of how you would evolve this architecture to support 1 million active users.

---

### **The Final Presentation**
You have **10 minutes total** (8 minutes for the talk/demo, 2 minutes for Q&A). 

* **Content:** Focus on a live demo of the core interactions, a walkthrough of your schema/indexes, and a discussion of your technical complexity component.
* **The Backup Plan:** Live deployments can be unpredictable. **Have your 3-minute demo video ready as a backup** and, if possible, have the environment running locally on your machine during your slot.
