import json

data_mess = {
    "help": """
    <b><em>Here’s what I can help you with</em></b>:
    <em>/create</em> - register your profile
    <em>/map</em> - display maps of all floors of the main building and help to find the road up to 4 buildings
    <em>/timetable</em> - show actual timetable on a particular day 
    <em>/info</em> - give a description of useful information for the study
    <em>/links_csu</em> - display links related to CSU and students' activity
    <em>/links_it</em> - display useful links that help in IT career development
    <em>/questions</em> - unswer the most popular questions
    <em>/spam</em> - send messages to each chat user (admins only)
    <em>/materials</em> - give usefull materials which can help you during studing
    <em>/help</em> - tell about my functions again 
        """,
    "csu": """
    <b><em>Websites related to CSU</em></b>:
        <u>Moodle CSU</u> - e-learning management system (here you can\
    find courses from teachers from different faculties)
        <u>Moodle IIT</u> - here you can find courses from teachers from IIT faculty
        <u>CSU site</u> - news site where you can find information about the CSU in general\
    (structure, schedule and more)
        <u>Scientific library CSU</u> - huge catalogue of e-books and other information sources
        <u>SCC (Student Creativity Center)</u> - here you can learn about the creative extracurricular life of the university
    (information on events, links to singing club, dancing club, etc.)
        <u>Trade union committee (vk)</u> - information for trade union participants (about events,
    benefits, how to join, etc.)
        
        <em>You want the references? Press /links_csu</em>
        """,
    "it": """
    <b><em>Shared resources (regardless of programming language)</em></b>:
        <u>Habr</u> - a site created for the publication of news, analytical articles, thoughts,\
    related to information technology and the Internet.
        <u>GitHub</u> - the largest web service for hosting IT projects and their joint development.\
    The site provides free source code, which you can read.
        <u>Metanit</u> - the site is devoted to various languages and programming technologies, computers,\
    mobile platforms and IT technologies with various guides and training materials, articles and examples
        <u>Summer Schools Open Lecture Hall from Yandex</u> - more than 150 lectures in online format, communication with top\
    experts from Yandex, the transfer of knowledge on demanded IT specialties and the solution of complex business cases
        <u>Cyberforum</u> - forum of programmers and system administrators, help in solving problems on \
    programming, mathematics, physics and other sciences, solving problems with computer, operating systems
        <u>Programmer library</u> - materials that will teach and help programming. Books and lectures,\
    videos and tips, knowledge tests and discussion of hot topics
        <u>Roadmap</u> - collection of road maps, guides and other educational content that \
    will help developers to choose the right path and guide their training.
        
        <em>Are you interested in? Press /links_it to get links</em>
        """,
    "que": """
    <b><em>What question do you want answered?</em></b>
        №1. How difficult it is to study?
        №2. Where can I find a timetable?
        №3. What are even and odd weeks? 
        №4. How to find your audience?
        №5. What is the  assessment week?
        №6. How is the session goes and what is it?
        №7. How to organize your time?
        №8. Where to look for somebody? 
        """,
    "answ1": """
    <b><em>Question 1</em></b>
        Depends on the student’s training (how well he studied at school, the speed of perception of information), but if \
    you really enjoy studied case, the study of even the most difficult subjects will bring joy
    """,
    "answ2": """
    <b><em>Question  2</em></b>
        Official website of TSU -> Students -> Timetables
    """,
    "answ3": """
    <b><em>Question  3</em></b>
       It can be said that the schedule of the university is composed with a period of 14 days (not 7, to which we are accustomed in school),\
    i.e. every 14 days the schedule is repeated.
    """,
    "answ4": """
    <b><em>Question  4</em></b>
        If the name of the audience starts with the letter A, for example A17, you should look for it in the lecture building.\
    If not, then in the main. In the theater building, usually no pairs. The first digit in the room\
    points to the floor, for example A24 is located on the 2nd floor, 315 on the third, and the auditorium\
    002 should be in the basement.
    """,
    "answ5": """
    <b><em>Question  5</em></b>
    The  assessment week is the same week with the same schedule. Just this week\
    prefects come to teachers and ask for a attestation . Attestation  - is some\
    preliminary results. If the student is attestated in the subject, it indicates that he is well learnt\
    training material and the likelihood that he will pass the test/examination on the subject well,\
    high enough. If the student is not certified in the subject, it indicates that he does not spend enought time for this\
    subject and he needs to pay more attention to its development. No one will scold for not reporting,\
    it is nessesary to give the student a grade on his intermediate grades.
    """,
    "answ6": """
    <b><em>Question  6</em></b>
        Session - is the period of time allocated for students to pass the exams for the current semester. During\
    the session, students do not have couples other than those in which they take exams.
    """,
    "answ7": """
    <b><em>Question  7</em></b>
        Time management is a key skill for a student. Scheduling taking into account all classes, homework and important\ 
        events will help you. It is also recommended to set priorities and allocate sufficient time for recreation and\
        self-development. Use calendars and scheduling applications to be more organized.
    """,
    "answ8": """
    <b><em>Question  8</em></b>
    331 - Yurina NA (questions on training activities)
    323 - Methodist (certificate of training)
    103 - profcom (ask all the questions about the trade union committee, join the trade union, arrange the material\
    assistance, arrange a ticket to the sanatorium - preventorium)
    """,
    "materials": """
    <b><em>Select the items you want to learn about:</em></b>
    1. English
    2. Discrete mathematics
    3. Computer science and programming
    4. History of Russia
    5. Linear algebra and analytic geometry
    6. Mathematical analysis
    7. Fundamentals of Russian statehood
    8. Right
    9. Modern information retrieval and processing technologies
    10. Physics
    """
}

with open('data.json', 'w') as file:
    json.dump(data_mess, file)