# LGBTQI Travel Safety API

---

## 1. Identification of the problem this app solves

This app is designed to be an indisposible tool to keep members of the LGBTQI community safe while they travel internationally. Due to a number of complex historical sociological reasons, LGBTQI+ peoples encounter environments of varying levels of safety when travelling overseas. Each country has it's own complex mesh of religions, social attitudes, levels of economic development, and other factors which contribute directly or indirectly to the safety of LGBTQI peoples specifically. Since all of these influences are hard to quantify into raw numbers which allow for statistical examinations of risk, I have decided to create an app that will function as a guide based on the personal subjective experiences of LGBTQI peoples in the countries they travel to, with an accompanying rating system out of 10 that will be calculated based on the ratings given by each reviewer. There will be a seperate rating for perceived safety, and perceived level of suitability for tourism.

---

## 2. Why is it a problem that needs solving?

The issue of LGBTQI peoples' safety is one of great importance. The majority of countries that currently exist do not have any legal protections at all for LGBTQI peoples, and many countries, particularly in northern Africa, the Middle East, and South East Asia, have especially hostile laws against LGBTQI peoples. Many LGBTQI peoples are, in return, equally hostile at the prospects of travelling to these places and as such shut down even the mentioning of travel in these regions. I do not support this stance. I believe all of us, no matter who we are, should be enthusiastic about travelling the world and seeing places different to where we grew up. I want to make this travel as safe as possible, and allow LGBTQI peoples to be as informed as possible when travelling. I have, through research, discovered a lack of resources for LGBTQI peoples in relation to travelling to/living in countries that are not LGBTQI friendly. I think this is a real shame and does a disservice to the community. LGBTQI peoples need as many resources as possible to keep them safe, and an attitude of dismissiveness and neglect towards the countries which may be hostile to LGBTQI peoples is akin to the proverbial emu sticking it's head in the sand. The neglect and ignorance towards this issue, and the consquent increase in risk to LGBTQI peoples that travel the world, is why this problem needs addressing, and I hope this app can, at least partly, address the issue. 

---

## 3. Why have you chosen this database system. What are the drawbacks compared to others?

---

## 4. Identify and discuss the key functionalities and benefits of an ORM

ORM has a number of key functionalities and benefits. According to Dua (2021), there are many benefits and functionalities of ORM such as simplified database access, increased developer productivity, platform independence, database schema management, and security benefits. ORM allows for a simplified way to access databases by allowing developers to interact with the database using language and concepts they already understand well from their knowledge in object-oriented programming. Many programmers are more comfortable with this as opposed to having to do everything with SQL quiries which they may not be as comfortable with using. In short, it allows developers to create and maintain database in language they already understand. ORM can also help to increase developer productivity by reducing the amount of code needed to interact with the database, in turn allowing developers to focus on writing code to model the business logic of their application (Reitz, 2018). Another benefit of ORM frameworks is that they are usually platform independent which means that they can work with all sorts of different database management systems. This consequently allows developers to switch between database management systems without having to rewrite their code. Furthermore, ORM frameworks can automatically create and maintain database schemas based on the application's object model, which eliminates the need for developers to manually create database schemas and maintain them over time (Dua, 2021). ORM can also increase security by reducing the risk of SQL injection attacks. This is due to the fact that ORM frameworks typically use "parameterised" queries that are less vulnerable to SQL injection attacks compared to raw SQL queries (Lasse, 2018).

---

## 5. Document all endpoints for your API

---

## 6. ERD

![ERD](./images/API%20ERD.png)

---

## 7. Detail any third party services that your app will use

---

## 8. Describe your projects models in terms of the relationships they have with each other

My project has 4 models: countries, cities, reviews, and users. Users are LGBTQI peoples who make a profile and can then review countries and/or cities based on their safety rating and their tourism rating. The relationships are as follows: 
Users leave reviews for countries or cities. (1 to many, users to reviews), countries have reviews left by users (1 to many, countries to reviews), cities have reviews left by users (1 to many, cities to reviews), and countries in turn have many cities (1 to many, countries to cities). 

## 9. Discuss the database relations to be implemented in your application

My application relies solely on one to many relationships. One to many relationships are an important fascet of data base design because they allow for the efficient and structured storage, retrieval and manipulation of data. (Date, 2003) One ot many relationships are noted for their ability to help ensure that data is consistent and accurate, as well as reducing data redundancy through the use of foreign keys. (Connolly & Begg, 2014) The enforecement of "referential integrity rules" helps to ensure that the data in the database is consistant by preventing the creation of "orphan records" and the deletion of records that are still being referenced somewhere else in the database. (Microsoft, 2021)

---

## 10. Describe the way tasks are allocated and tracked in your project

Firstly, I will break down the development of my api into smaller tasks. By developing little building blocks, I can tackle the api one step at a time. 
Next, I will prioritise the tasks I have developed, based on importance and complexity. Next, I will set deadlines for each task to ensure that the project stays on track. 
Next, I will use Trello to help track the progress of each task and also the api as a whole. I can use this to identify and address any roadblocks I may encounter. 
Finally, I will be flexible. I may need to adapt the project plan based on changing priorities, or unexpected issue, or new requirements, etc. 

## Sources

<ol>
<li>Dua, S. (2021). Benefits of ORM (Object Relational Mapping). Towards Data Science.</li>
<br>
<li>Reitz, K. (2018). What is an ORM and Why You Should Use it. Towards Data Science.</li>
<br>
<li>Lasse, K. (2018). What is an ORM, and why is it important?. freecodecamp.
</li>
<br>
<li>Date, C. J. (2003). An introduction to database systems. Addison-Wesley Longman Publishing Co., Inc.
</li>
<br>
<li>Connolly, T., & Begg, C. (2014). Database systems: a practical approach to design, implementation, and management. Pearson.</li>
<br>
<li>Microsoft. (2021). One-to-Many Relationships. Microsoft Docs.</li>
<br>
<ol>