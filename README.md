# Harvard CS50 Web Final Project: Dog-Walking Coordination Web App
**Submission by Benedict Lee**

### My dog, a Female British Bulldog named Diva!
![My dog, a Female British Bulldog named Diva!](./images/diva-picture.jpg)

## 1. Motivation and Purpose
The key motivation for this web app is to not only create something adequately complex for the final project, but to also build something useful to me and my family! It has been extremely rewarding to be able to put everything I've learned from university and from this course into building something tangible, that also provides utility to me.

This web application aims to be one centralized platform to track, schedule and allocate dog walking duties within the family. It will allow users to manage dog profiles, assign or take up walk responsibilities, and track the dog-walking history.

## 2. Distinctiveness and Complexity

### Distinctiveness
I believe my project satisfies the distinctiveness requirements, because this Dog-Walking Coordination Web App is uniquely designed to cater to the specific needs of managing dog-walking schedules within a family. Unlike previous projects in this course, this application introduces several distinct features:

- **Walk Scheduling & Tracking System**
  - Similar to previous projects, the web app allows family members to create accounts, log in securely.
  - However, the similarities end there: Users can schedule walks, view upcoming walks in a calendar format, and track the history of past walks. The scheduling system is designed to handle multiple walks per day and provides a clear overview of the dog-walking duties within the family.
  - The visual layout and navigation of the web app had to change to accommodate the calendar view and scheduling system, further adding to distinctiveness from previous projects

- **Centralized Dog Profile Management**
  - Each dog has a detailed profile that includes its name, breed, age, owners, a picture URL, and any special care instructions. This allows for comprehensive management of multiple dogs within a single platform.
  - Users can manage dog profiles on the Dogs page, allowing them to view and delete dog profiles.

- **User Profiles with Walk Tracking**
  - Each user has a profile displaying their username, email address, profile picture, and the number of walks completed.
  - By displaying the number of walks completed, it gamifies this aspect of daily tasks, encouraging family members to participate more actively in dog-walking duties.

### Complexity
I believe my project satisfies the complexity requirements as it surpasses the complexity of previous projects through several more advanced technical implementations:

- **Complex Database Relationships**
  - The app builds on the complexity of previous projects by using four interconnected models (User, Dog, Walk, Date_of_walks) with intricate relationships to ensure data integrity and efficient querying. 
  - For example, each Walk is linked to both a User and a Dog, and the Date_of_walks model aggregates walk data by date to optimize display and management.
  - This database design was a step-up in terms of complexity from previous projects, and incorporated several database design principles like database normalization.
  - You can find the ER Diagram for the database below, in section 3.

- **Advanced JavaScript Integration, for greater user experience**
  - The front-end heavily relies on JavaScript to manage dynamic interactions. This includes using the Fetch API to handle asynchronous operations such as updating profile pictures, removing dogs, as well as adding and deleting walks. This level of JavaScript integration is much more complex than any previous project.
  - The web app also includes intuitive navigation aids, such as a back button to return to the calendar view and confirmation dialogs for actions like deleting walks or removing dogs. These features are implemented using JavaScript, to enhance usability and ensure smooth interaction with the app.
  - The more advanced used of Javascript in the app required me to implement more API functions in my views.py, to seamlessly link my backend and frontend together.
  - More API functions also means more endpoint security, with elements like CSRF tokens and decorating with @login_required to ensure only authenticated users can access the main features. Additionally, authorization checks are implemented to enforce correct access levels.

- **Mobile Responsiveness**
  - Ensuring the application is mobile-responsive required extensive use of CSS media queries and responsive design principles. The layout adapts seamlessly to different screen sizes, providing a consistent user experience across devices.
  - On a large screen like a laptop/PC, the website expands to fill the space and look visually pleasing.
  - When viewed on a smaller screen like a handphone, the website will scale down to fit all the navigation tabs vertically instead of horizontally, and the calendar view also scales down to fit one screen.

- **Custom CSS styling, without Bootstrap**
  - To achieve the look and feel I desired, I chose not to use Bootstrap to give me greater freedom in styling.
  - As a result, more time and effort was placed into designing and customizing my website with CSS. 


## 3. Database Schema
![My Database ER Diagram](./images/CS50%20Web%20Capstone%20Schema.png)

## 4. Technical Specifications

1. **Models:**
   - **User:**
     - Stores user credentials such as username, email, password, along with statistics like the number of walks completed and a URL to their profile picture.
   - **Dog:**
     - Contains details about each family dog including name, breed, age, owners, a picture URL, and any specific care instructions.
   - **Walk:**
     - Tracks individual walks with attributes like walkID, date, time, duration, the dog walked, and completion status.
   - **Date_of_walks:**
     - Aggregates walk data by date to facilitate efficient display and management.

2. **Calendar:**
   - The homepage features columns displaying daily walks, where each column represents a day with scheduled walks.
   - Implements pagination to display a week's worth of walks (7 days per page), enhancing usability and navigation.
   - Users can click on any walk to view detailed information without refreshing the entire page, utilizing JavaScript for seamless updates.
   - Includes navigation aids like a back button for returning to the calendar view and a delete button to remove walks, all updated in real-time.

3. **Profile:**
   - Provides users with a dedicated profile page for managing their account information.
   - Displays essential details such as username, profile picture (rendered via URL), email address, and total walks completed.
   - Offers an edit button to update profile pictures, guiding users through a streamlined process.
   - When editing, users view all existing details before entering a new image URL, ensuring clarity and ease of use.
   - Leverages JavaScript to update profile views dynamically, enhancing user interaction by avoiding full-page reloads.
   - Restricts editing capabilities: users can change their own profile pictures, but not others.

4. **Dogs:**
   - Presents a comprehensive list of all family dogs, showcasing details like name, breed, age, owners, and specific care instructions.
   - Allows users to add new dogs via an intuitive interface accessed through an 'add new dog' button, which redirects to a dedicated page for input.
   - Allows users to remove dogs via a 'remove dog' button, which asks for confirmation using Javascript to render the view without needing to reload the page. Once confirmed, the fetch API is used to perform the database modifications, before reloading the dogs view to show the changes.
   - Integrates API calls (fetch) to connect frontend actions seamlessly with backend operations, ensuring efficient data management and synchronization.

5. **Django Admin:**
   - Empowers administrators with Django's built-in admin interface to manage users, dogs, and walks efficiently.

6. **API Integration:**
   - Utilizes APIs to dynamically link JavaScript-rendered frontend pages with Python backend functionality.
   - Enhances user experience by enabling rapid updates when editing profiles, removing dogs, or deleting walks without necessitating page reloads.
   - Implements the fetch API to transmit user inputs to the backend for database modifications, and then redirects users to relevant pages upon completion.

7. **Security and Safety**
    - All main features can only be accessed once logged in, to prevent outsiders from viewing a family's walking history
    - All functions which require the user to be logged in are decorated with @login_required to help ensure security
    - Conditional checks implemented to ensure correct authorization levels before executing actions
    - CSRF tokens used when submitting forms, to ensure safety and security


## 5. What's contained in each file?
1. *urls.py*
    - Contains all of the paths I created, both for rendering pages and for API calls. In total, there are 13 paths created

2. *views.py*
    - Corresponding to the 13 paths created, there are 13 functions defined in views.py, of which 5 are API calls and the remaining 8 are for rendering views. The database modification is handled here, mainly in the API calls.

3. *models.py*
    - Here I created my 4 models, and defined all the different attributes for them

4. **Templates**
    - *layout.html*: this file was the layout from which all other html files inherited. It's also where the structure of the top navbar was defined.
    - *index.html*: landing page of the application, this file displays the calendar page for the app. Since this was a tracking app, I decided the intuitive thing to have was to open the calendar as the default page. This page will not display the calendar if the user is not logged in.
    - *login.html*: interface for users to log in.
    - *register.html*: interface for users to register for an account.
    - *profile.html*: defined the structure of the profile page here, where users can view their own profile and edit their profile picture.
    - *view_dogs.html*: defined the structure of the dog page here, where users can view the dogs in the family and delete/add dogs.
    - *new_dog.html*: view for when the user wants to add a new dog. contains a form where users can fill up all the fields needed to add a new dog, and links to an API call I defined
    - *new_walk.html*: view for when the user wants to add a new walk. contains a form where users can fill up all the fields needed to add a new walk, and links to an API call I defined

5. **Static**
    - *styles.css*: my defined styles for the entire program. Since I chose not to use bootstrap, this file is very long as it has different styles for all the different pages.
    - *index.js*: Javascript file where I handle all of the AJAX functionality for the index page (calendar view). This includes clicking on any of the walks, and handling all the HTML and further Javascript for those views. (back button and delete button)
    - *edit_button.js*: Javascript file where I handle all of the AJAX functionality on the Profile view. This allows users to click edit, and change their profile picture without reloading the page.
    - *remove_dog.js*: Javascript file where I handle all of the AJAX functionality on the Dogs view. Users can remove a dog without reloading the page, with this file.

6. **Root Directory**
    - *images folder*
      - *diva-picture.jpg*: one of my favourite pictures of my dog to be displayed in this README
      - *CS50 Web Capstone Schema.png*: Image of the ER diagram of the database utilized in this project
    - *README.md*: detailed description of this project which you are reading now :D


## 6. How to Run the Application
There are no special libraries installed, so as long as you have Python and Django installed there should be no issue!

1. Clone the repository:

`git clone https://github.com/ivecookies/cs50web-capstone`

`cd dog-walking-app`

2. Run migrations to set up the database:
python manage.py makemigrations
python manage.py migrate

3. Start the Django development server:
python manage.py runserver

4. Open your web browser and navigate to `http://localhost:8000` to view the application.

## Author
Benedict Lee
- [GitHub](https://github.com/ivecookies)
- [LinkedIn](https://www.linkedin.com/in/benedict-lee-0a0868241/)